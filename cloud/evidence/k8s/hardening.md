# Local workload hardening

Context: local `kind-grp01` web deployment on 2026-11-25 UTC. Original recording: `hardening.session`; PNG: genuine render of that recording.

Commands: `kubectl -n grp01-demo get deployment grp01-web -o yaml | sed -n '30,80p'`; `kubectl auth can-i get secrets -n grp01-demo --as system:serviceaccount:grp01-demo:grp01-web`; `kubectl -n grp01-demo get secret grp01-demo-secret -o custom-columns=NAME:.metadata.name,TYPE:.type`; `kubectl get namespace grp01-demo --show-labels`. Exact commands, full outputs, `[GRP01]` prompt, and `date -u` appear in the PNG.

Expected: restricted pod security, resources bounded, no workload API permission to read Secrets, and a runtime-created Secret referenced without printing its value. Actual: UID 10001, non-root, read-only filesystem, no privilege escalation, `ALL` capabilities dropped, `RuntimeDefault` seccomp, CPU/memory requests and limits, `automountServiceAccountToken: false`, `kubectl auth can-i` returned `no`, the Secret exists, and the namespace has `restricted` enforcement labels.

Interpretation: the local workload configuration and API authorization match the intended controls. Kubernetes Secrets are not encrypted at rest by this local demo; no production-data claim is made.
