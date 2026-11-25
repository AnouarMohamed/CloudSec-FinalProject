# Live terminal capture — Kubernetes workload security settings

- **Context:** Phase F local kind cluster, `grp01-demo/grp01-web` deployment, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq -c '{pod:.spec.template.spec.securityContext,container:.spec.template.spec.containers[0].securityContext}'`; `rtk proxy kubectl -n grp01-demo get deployment grp01-web -o json | jq -c '.spec.template.spec.containers[0].resources'`.
- **Expected:** Non-root, restricted runtime, read-only filesystem, dropped capabilities, and bounded resources.
- **Actual:** Pod settings include UID/GID `10001`, `runAsNonRoot=true`, and `RuntimeDefault` seccomp. Container settings include `allowPrivilegeEscalation=false`, `drop=["ALL"]`, and `readOnlyRootFilesystem=true`; limits are `100m` CPU/`64Mi` memory, requests `10m` CPU/`16Mi` memory.
- **Interpretation:** The deployment specification contains the required controls; this image does not itself demonstrate admission rejection or runtime escape resistance.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-pod.session](../terminal-live/ptyxis-pod.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
