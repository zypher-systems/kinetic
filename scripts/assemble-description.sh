#!/usr/bin/env bash
# Stage Fedora's vendored kiwi descriptions and Kinetic's own files into a
# single kiwi description directory (out/description by default).
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

dest="${1:-${KINETIC_DESC_DIR}}"

rm -rf "${dest}"
mkdir -p "${dest}"

cp -a "${KINETIC_ROOT}/kiwi/fedora/." "${dest}/"

# Kinetic's config.sh replaces Fedora's and calls it from inside the image
install -D -m 0755 "${KINETIC_ROOT}/kiwi/fedora/config.sh" "${dest}/root/kinetic-build/fedora-config.sh"
install -m 0755 "${KINETIC_ROOT}/kiwi/config.sh" "${dest}/config.sh"

cp -a "${KINETIC_ROOT}/kiwi/Kinetic.kiwi" "${dest}/"
cp -a "${KINETIC_ROOT}/kiwi/kinetic" "${dest}/"

if [[ -d "${KINETIC_ROOT}/kiwi/root" ]]; then
	cp -a "${KINETIC_ROOT}/kiwi/root/." "${dest}/root/"
fi

echo "Description staged in ${dest}"
