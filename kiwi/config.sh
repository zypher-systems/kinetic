#!/bin/bash
# Runs inside the image root during the kiwi build.
# Fedora's config.sh runs first, unchanged; Kinetic's own steps follow.

set -euxo pipefail

test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

bash /kinetic-build/fedora-config.sh
rm -rf /kinetic-build

echo "Configure Kinetic: [$kiwi_iname]-[$kiwi_profiles]..."

exit 0
