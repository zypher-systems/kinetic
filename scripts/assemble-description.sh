#!/usr/bin/env bash
# Stage Fedora's vendored kiwi descriptions and Kinetic's own files into a
# single kiwi description directory (out/description by default).
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

dest="${1:-${KINETIC_DESC_DIR}}"

rm -rf "${dest}"
mkdir -p "${dest}"

cp -a "${KINETIC_ROOT}/kiwi/fedora/." "${dest}/"

# Fedora's ISO boot menu defaults to its second entry, which checks the whole
# medium before starting: a minute or more for an image this size. Kinetic
# starts directly; the check stays in the menu. Done on the staged copy, so
# the vendored description stays as Fedora ships it.
grub_template="${dest}/grub-x86.cfg.iso-template"
sed -i 's/^set default="1"$/set default="0"/' "${grub_template}"
grep -q '^set default="0"$' "${grub_template}" || { echo "Could not set the ISO boot menu default in ${grub_template}" >&2; exit 1; }

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
