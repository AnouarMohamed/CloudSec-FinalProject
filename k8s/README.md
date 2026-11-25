# GRP01 local Kubernetes security demo

This bonus uses a local kind cluster. It creates no AWS Kubernetes, compute, load balancer, or NAT resource. `kind.yaml` disables kind's default CNI so Calico can enforce the NetworkPolicies; without an enforcing CNI, the policy YAML would not prove traffic isolation. The cluster name is `grp01`.

## Controls

- Namespace `grp01-demo` enforces Kubernetes Pod Security `restricted`.
- The web and client pods use dedicated service accounts, with API tokens not mounted. There are no RoleBindings for them, so they receive no application API permissions. Verify with `kubectl auth can-i get secrets -n grp01-demo --as system:serviceaccount:grp01-demo:grp01-web` (expected `no`).
- The web and clients run as UID 10001, use a read-only root filesystem, disallow privilege escalation, drop all capabilities, and use the runtime default seccomp profile. CPU and memory requests and limits are defined.
- A namespace default-deny NetworkPolicy blocks all ingress and egress. Two explicit policies permit only the `access=allowed` client to reach TCP 5678 on the web pod. The `access=blocked` client has no egress permit and is rejected by the web ingress policy too.
- The fictional demo Secret is generated at runtime by `create_secret.py`, piped to `kubectl` in memory, and referenced through `secretKeyRef`. The value is not committed, logged, or printed. This is a demo secret, not a production credential.

## Reproduce

```sh
kind create cluster --name grp01 --config k8s/kind.yaml
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.33.0/manifests/calico.yaml
kubectl -n kube-system rollout status daemonset/calico-node --timeout=300s
kubectl create namespace grp01-demo
kubectl label namespace grp01-demo pod-security.kubernetes.io/enforce=restricted pod-security.kubernetes.io/audit=restricted pod-security.kubernetes.io/warn=restricted
python3 k8s/create_secret.py
kubectl apply -f k8s/demo.yaml
kubectl -n grp01-demo rollout status deployment/grp01-web --timeout=180s
kubectl -n grp01-demo wait --for=condition=Ready pod/grp01-allowed pod/grp01-blocked --timeout=180s
```

The namespace also appears in `demo.yaml`, so the later apply reconciles its labels. The evidence sessions show the commands actually run.

## Proof and limits

The [network-policy capture](../cloud/evidence/k8s/network-policy.png) shows both clients calling the same healthy web pod IP. The allowed client received `GRP01 web ready`; the blocked client timed out with exit code 28. The [hardening capture](../cloud/evidence/k8s/hardening.png) shows the restricted workload settings and `kubectl auth can-i` returning `no` for Secret reads. The original `.session` files and captions are beside the PNGs. The demo is local and does not claim to secure a managed cluster.

Delete local resources with `kind delete cluster --name grp01` after evidence review. This removes only the local demo cluster.

References: [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/), [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/), [Secrets good practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/), [Calico on kind](https://docs.tigera.io/calico/latest/getting-started/kubernetes/kind).
