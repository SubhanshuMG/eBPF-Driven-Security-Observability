import os
import re
from flask import Flask, request, jsonify
from kubernetes import client, config
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# In-cluster config by default
try:
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    app.logger.info("Loaded in-cluster config")
except Exception:
    # for local testing fallback to kubeconfig
    config.load_kube_config()
    v1 = client.CoreV1Api()
    app.logger.info("Loaded kubeconfig")

def extract_pod_info(payload):
    falco_result = payload.get("FalcoResult") or payload.get("falco_result") or payload
    container = falco_result.get("container") or falco_result.get("container_info") or {}
    pod = container.get("pod") or container.get("name") or container.get("pod_name") or container.get("name")
    namespace = container.get("namespace") or container.get("ns") or falco_result.get("namespace")

    if not pod or not namespace:
        output = falco_result.get("Output") or falco_result.get("output") or falco_result.get("message") or ""
        pod_match = re.search(r"pod=([A-Za-z0-9\-\_\.]+)", output)
        ns_match = re.search(r"namespace=([A-Za-z0-9\-\_\.]+)", output)
        if pod_match:
            pod = pod_match.group(1)
        if ns_match:
            namespace = ns_match.group(1)

    return pod, namespace

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(force=True, silent=True) or {}
    app.logger.info("Received webhook: keys=%s", list(payload.keys()))
    try:
        pod, namespace = extract_pod_info(payload)
        if not pod or not namespace:
            app.logger.warning("Could not extract pod/namespace from payload")
            return jsonify({"status": "no-pod-info"}), 200

        body = {"metadata": {"labels": {"compromised": "true"}}}
        resp = v1.patch_namespaced_pod(name=pod, namespace=namespace, body=body)
        app.logger.info("Patched pod %s/%s", namespace, pod)
        return jsonify({"status": "patched", "pod": pod, "namespace": namespace}), 200
    except client.exceptions.ApiException as e:
        app.logger.exception("Kubernetes API error")
        return jsonify({"status": "k8s-error", "error": str(e)}), 500
    except Exception as e:
        app.logger.exception("Unhandled exception processing webhook")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
