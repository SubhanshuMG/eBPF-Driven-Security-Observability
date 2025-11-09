# Beyond the Kernel: eBPF-Driven Security Observability in Cloud-Native Environments

*eBPF as a real-time security sensor for AWS EKS clusters.*

---

## Part 1: Concepts and Architecture

### The Security Blind Spot
Cloud-native infra often misses kernel-level events. eBPF lets you attach tiny programs to kernel hooks so you can see syscalls, sockets and TLS handshakes as they happen.

### eBPF as a Real-Time Sensor
In an EKS node, eBPF hooks into syscalls (execve, connect, open), the networking stack (TC/XDP), and LSM hooks. Events are enriched with Kubernetes metadata and fed to Falco.

### Falco: Rule Engine on Top of eBPF
Falco consumes eBPF events and applies detection rules. Example:

```yaml
- rule: Shell in Container
  desc: Detect spawning a shell inside a container
  condition: container.id != host and proc.name in (bash, sh, zsh)
  output: "Shell spawned in container (user=%user.name, command=%proc.cmdline, container=%container.name)"
  priority: WARNING
```

### Architecture Diagrams
- Minimalistic schematic: `diagrams/minimalistic.png`
- Modern cloud architecture: `diagrams/modern-cloud.png`

![Modern Cloud Architecture](diagrams/modern-cloud.png)

Flow summary:
1. Pods emit syscalls and TLS events.
2. eBPF Agents intercept events in kernel.
3. Falco applies rules and enriches with pod metadata.
4. Alerts are forwarded to Slack, Prometheus, or a Remediator.
5. Cilium or eBPF-LSM can block or isolate a compromised pod.

---

## Part 2: Implementation and Testing

### Deploy Falco (Helm)
Use the provided `charts/falco-values.yaml` and install Falco:

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco -n falco --create-namespace -f charts/falco-values.yaml
```

### Python BCC Agent
A DaemonSet runs a Python BCC agent to demonstrate custom probes; it detects outbound connections to port 4444.

### Falco Sidekick + Remediator
Falco Sidekick forwards alerts to Slack and to the Remediator webhook. The repository contains:
- `remediator/` — Python remediator for quick deployments.
- `operator-remediator/` — Go operator scaffold for hardened production use.

### Testing
1. Deploy a test pod: `kubectl run test-shell --image=ubuntu -- sleep 3600`
2. Inside pod: `nc 1.2.3.4 4444`
3. Observe Falco alerts, Slack notification, Remediator patching pod with label `compromised=true`.

### Automated Isolation
Cilium policy in `manifests/cilium-block-policy.yaml` isolates pods labeled `compromised=true`.

---

## Appendix: Operator & CI
This repo includes a minimal Go operator under `operator-remediator/` and a GitHub Actions workflow to build and push images.

---

*Prepared for publication on blogs.subhanshumg.com*  
