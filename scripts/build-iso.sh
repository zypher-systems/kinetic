#!/usr/bin/env bash
# Build the Kinetic live ISO with kiwi. Needs root:
#
#   sudo ./scripts/build-iso.sh
#
# Installs kiwi on the host the first time. The ISO lands in out/, owned by
# the user who ran sudo.
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

if [[ ${EUID} -ne 0 ]]; then
	echo "Run with sudo: sudo $0" >&2
	exit 1
fi

owner="${SUDO_USER:-root}"
build_dir="/var/tmp/kinetic-build"
log="${KINETIC_OUT}/build.log"
started=${SECONDS}

deps=(kiwi-cli kiwi-systemdeps kiwi-selinux distribution-gpg-keys)
missing=()
for pkg in "${deps[@]}"; do
	rpm -q "${pkg}" >/dev/null 2>&1 || missing+=("${pkg}")
done
if ((${#missing[@]})); then
	echo "==> Installing build dependencies: ${missing[*]}"
	dnf -y install "${missing[@]}"
fi

# A killed kiwi run can leave /dev, /proc, and /sys bind-mounted inside the
# old image root. Unmount them first, and never let rm cross into a mount.
if [[ -d "${build_dir}" ]]; then
	echo "==> Clearing previous build in ${build_dir}"
	findmnt --list --noheadings --output TARGET | grep "^${build_dir}/" | sort -r | while read -r mnt; do
		umount --recursive --lazy "${mnt}" || true
	done
	rm -rf --one-file-system "${build_dir}"
fi

sudo -u "${owner}" mkdir -p "${KINETIC_OUT}"
sudo -u "${owner}" "${KINETIC_ROOT}/scripts/assemble-description.sh"

echo "==> Building ${KINETIC_ISO_NAME} (log: ${log})"
kiwi-ng --profile="${KINETIC_PROFILE}" --type=iso --kiwi-file=Kinetic.kiwi --logfile="${log}" \
	system build \
	--description "${KINETIC_DESC_DIR}" \
	--target-dir "${build_dir}" \
	--set-type-attr "volid=${KINETIC_VOLID}" \
	--set-type-attr "application_id=${KINETIC_APPID}" \
	--set-type-attr "publisher=${KINETIC_PUBLISHER}"

iso="$(find "${build_dir}" -maxdepth 1 -name '*.iso' -print -quit)"
if [[ -z "${iso}" ]]; then
	echo "kiwi finished but produced no ISO; see ${log}" >&2
	exit 1
fi

mv -f "${iso}" "${KINETIC_ISO}"
(cd "${KINETIC_OUT}" && sha256sum "${KINETIC_ISO_NAME}" > "${KINETIC_ISO_NAME}.sha256")
chown "${owner}:" "${KINETIC_ISO}" "${KINETIC_ISO}.sha256" "${log}"

elapsed=$((SECONDS - started))
echo "==> Done in $((elapsed / 60))m $((elapsed % 60))s: ${KINETIC_ISO} ($(du -h "${KINETIC_ISO}" | cut -f1))"
