# eBPF + Falco E2E Reference for AWS EKS

This repository is a packaged deliverable containing:

- A ready-to-deploy reference implementation (Falco + eBPF + Python BCC + Falco Sidekick + Remediator)
- Helm values and Falco rules
- A polished, publish-ready article (Markdown) that embeds architecture diagrams
- A hardened operator-style remediator scaffold (Go operator) with CRD and RBAC
- CI (GitHub Actions) workflow for building and pushing images
- Scripts to deploy and cleanup a test environment on EKS

Files of interest:
- `article/published_article.md` — polished article with embedded diagram references
- `charts/` — Helm override values for Falco & Falco Sidekick
- `manifests/` — Falco rules ConfigMap, python-bcc DaemonSet, Cilium policy, etc.
- `remediator/` — Python remediator service (for quick start)
- `operator-remediator/` — Go operator scaffold for hardened remediator (controller)
- `diagrams/` — minimalistic and modern cloud architecture PNGs

> NOTE: Replace placeholder values (container registry, Slack webhook) before deploying. Test in a non-production environment first.
