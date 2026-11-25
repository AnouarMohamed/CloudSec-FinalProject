# Live terminal capture — workload RBAC, Secret metadata, namespace policy

- **Context:** Phase F local kind cluster `grp01`, namespace `grp01-demo`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy kubectl auth can-i get secrets -n grp01-demo --as system:serviceaccount:grp01-demo:grp01-web`; `rtk proxy kubectl -n grp01-demo get secret grp01-demo-secret -o custom-columns=NAME:.metadata.name,TYPE:.type`; `rtk proxy kubectl get namespace grp01-demo --show-labels`.
- **Expected:** Web ServiceAccount lacks Secret-reading API permission; runtime Secret exists; Pod Security namespace labels enforce restricted level.
- **Actual:** `can-i` returned `no`; `grp01-demo-secret` is `Opaque`; namespace labels include `enforce=restricted`, `audit=restricted`, and `warn=restricted`.
- **Interpretation:** API authorization and namespace labels are observed. Listing Secret metadata does not disclose or prove the secret value.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
