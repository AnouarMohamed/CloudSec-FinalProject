#!/usr/bin/env bash
# This shell changes only its isolated UTS namespace hostname. It does not
# rename the user's physical host or imply that this is a project VM.
set -eu
cd /home/anouar/Projects/cloudkhoudali
exec unshare --user --map-root-user --uts bash -c 'hostname atl-cloud-GRP01; export PS1="[GRP01] \h\$ "; export AWS_PAGER=""; exec bash --noprofile --norc -i'
