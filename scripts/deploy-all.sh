#!/usr/bin/env bash
set -euo pipefail

REGISTRY=${1:-REPLACE_WITH_REGISTRY}

echo "[1/8] Ensure remediator images and python-bcc images are pushed to registry"
echo "Please build and push images or run CI before proceeding."

echo "[2/8] Create remediator namespace and apply RBAC"
kubectl apply -f manifests/remediator/remediator-deployment.yaml
kubectl apply -f manifests/remediator/remediator-rbac.yaml

echo "[3/8] Update images if you have registry argument"
kubectl -n remediator set image deployment/remediator remediator=${REGISTRY}/remediator:latest || true
kubectl -n kube-system set image daemonset/python-bcc python-bcc=${REGISTRY}/python-bcc:latest || true

echo "[4/8] Deploy python-bcc DaemonSet"
kubectl apply -f manifests/python-bcc-daemonset.yaml

echo "[5/8] Install Falco (Helm) with overrides"
helm upgrade --install falco falcosecurity/falco -n falco --create-namespace -f charts/falco-values.yaml

echo "[6/8] Apply falco rules configmap"
kubectl apply -f manifests/falco-rules-configmap.yaml
kubectl -n falco rollout restart daemonset/falco

echo "[7/8] Install Falco Sidekick"
helm upgrade --install falcosidekick falcosecurity/falcosidekick -n falco -f charts/falcosidekick-values.yaml

echo "[8/8] Deploy Cilium policy (optional)"
kubectl apply -f manifests/cilium-block-policy.yaml || true

kubectl get pods -A
echo "Deploy complete. Verify pods and logs."
