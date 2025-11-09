#!/usr/bin/env bash
set -euo pipefail

echo "Deleting Falco / Falco Sidekick"
helm uninstall falco -n falco || true
helm uninstall falcosidekick -n falco || true
kubectl delete ns falco || true

echo "Deleting remediator"
kubectl delete -f manifests/remediator/remediator-deployment.yaml || true
kubectl delete -f manifests/remediator/remediator-rbac.yaml || true
kubectl delete ns remediator || true

echo "Deleting python-bcc daemonset"
kubectl delete -f manifests/python-bcc-daemonset.yaml || true

echo "Deleting cilium policy"
kubectl delete -f manifests/cilium-block-policy.yaml || true

echo "Cleanup complete."
