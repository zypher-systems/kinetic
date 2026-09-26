#!/bin/bash
# Runs inside the image root during the kiwi build.
# Fedora's config.sh runs first, unchanged; Kinetic's own steps follow.

set -euxo pipefail

test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

bash /kinetic-build/fedora-config.sh
rm -rf /kinetic-build

echo "Configure Kinetic: [$kiwi_iname]-[$kiwi_profiles]..."

#======================================
# Containers and VMs without sudo
#--------------------------------------
## Users created by Plasma Setup on first boot join docker and libvirt
sed -i -e 's/^UserGroups=.*/UserGroups=wheel,docker,libvirt/' /etc/xdg/plasmasetuprc
## Start Docker on first use rather than at every boot
systemctl enable docker.socket

exit 0
