# Local NetworkPolicy test

Context: local `kind-grp01` cluster with Calico, running restricted GRP01 demo pods on 2026-11-25 UTC. Original recording: `network-policy.session`; PNG: genuine render of that recording.

Commands: `kubectl -n grp01-demo get pods -o custom-columns=NAME:.metadata.name,IP:.status.podIP`; `kubectl -n grp01-demo get networkpolicy`; and `kubectl exec` from `grp01-allowed` and `grp01-blocked` to the same `http://192.168.54.5:5678`, with exact options visible in the image. The `[GRP01]` prompt and `date -u` are shown.

Expected: the explicitly allowed client gets the web response; the blocked client cannot connect. Actual: allowed returned `GRP01 web ready`; blocked timed out after 5002 ms with exit code 28. The three policies (default deny, web ingress, allowed-client egress) were listed in the same recording.

Interpretation: Calico enforced the intended traffic boundary for this local test. The pod IP is ephemeral; query the current IP before repeating the command.
