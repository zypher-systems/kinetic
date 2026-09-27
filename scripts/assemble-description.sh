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

# Fill in local paths: the signing keys and the locally built package repo.
# The check runs in a container, where these live elsewhere.
root_path="${KINETIC_ASSEMBLE_ROOT:-${KINETIC_ROOT}}"
repo_path="${KINETIC_ASSEMBLE_REPO_DIR:-${KINETIC_REPO_DIR}}"
find "${dest}/kinetic" -name '*.xml' -exec sed -i \
	-e "s|@KINETIC_ROOT@|${root_path}|g" \
	-e "s|@KINETIC_REPO_DIR@|${repo_path}|g" {} +

echo "Description staged in ${dest}"
