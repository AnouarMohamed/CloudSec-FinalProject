# Live terminal capture — NetworkPolicy allow and deny

- **Context:** Phase F local kind cluster `grp01`, namespace `grp01-demo`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy kubectl -n grp01-demo get pods -o custom-columns=NAME:.metadata.name,IP:.status.podIP`; `rtk proxy kubectl -n grp01-demo get networkpolicy`; `rtk proxy kubectl -n grp01-demo exec grp01-allowed -- curl --max-time 5 -sS http://192.168.54.10:5678`; `rtk proxy kubectl -n grp01-demo exec grp01-blocked -- curl --max-time 5 -sS http://192.168.54.10:5678`.
- **Expected:** Allowed client connects to the web pod; blocked client cannot connect to the same endpoint.
- **Actual:** Three policies include `grp01-default-deny`; allowed client returned `GRP01 web ready`; blocked client timed out after 5002 ms with exit code 28.
- **Interpretation:** This live test supports the NetworkPolicy effect on the local cluster at that time. Pod IP is ephemeral; obtain it again before repeating the commands.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
