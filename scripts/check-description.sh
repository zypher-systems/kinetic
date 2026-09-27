#!/usr/bin/env bash
# Check the image description without root, in a rootless podman container:
# validate the kiwi XML, resolve the ISO's full package set with dnf the way
# kiwi's build does (groups, bootstrap, and exclusions included), and check
# what must and must not be in the image. Run build-rpms.sh first.
#
#   ./scripts/check-description.sh            # writes out/packages.txt
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

image="localhost/kinetic-builder:44"
check_dir="${KINETIC_OUT}/description-check"

[[ -f "${KINETIC_REPO_DIR}/repodata/repomd.xml" ]] || { echo "No local package repo; run ./scripts/build-rpms.sh first" >&2; exit 1; }

KINETIC_ASSEMBLE_ROOT=/check KINETIC_ASSEMBLE_REPO_DIR=/check/repo \
	"${KINETIC_ROOT}/scripts/assemble-description.sh" "${check_dir}" >/dev/null
cp -a "${KINETIC_REPO_DIR}" "${check_dir}/repo"
cp -p "${KINETIC_ROOT}/scripts/resolve-packages.py" "${check_dir}/"

podman build --quiet --tag "${image}" "${KINETIC_ROOT}/containers/builder" >/dev/null

podman run --rm \
	--volume "${check_dir}:/check:Z" \
	--volume kinetic-resolve-cache:/var/cache/kinetic-resolve \
	"${image}" bash -euo pipefail -c "
		kiwi-ng --profile='${KINETIC_PROFILE}' --type=iso --kiwi-file=Kinetic.kiwi image info --description /check >/dev/null
		echo 'Image description: valid'
		python3 /check/resolve-packages.py /check Kinetic.kiwi '${KINETIC_PROFILE}' /check/packages.txt
	"

cp "${check_dir}/packages.txt" "${KINETIC_OUT}/packages.txt"

# The image must include these...
required=(
	zypheros-release zypheros-logos kinetic-repos kinetic-backgrounds kinetic-plasma
	kinetic-shell kinetic-agents kinetic-snapshots plasma-desktop plasma-login-manager
	anaconda-live chromium ghostty codium docker-ce podman distrobox virt-manager
	qemu-kvm fish starship ffmpeg mesa-va-drivers-freeworld libreoffice-writer gimp
	inkscape blender obs-studio tailscale syncthing snapper btrfs-assistant
	webkit2gtk4.1-devel rustup firewalld jetbrains-mono-fonts
)
# ...and must not include these
excluded=(
	firefox kmail kontact korganizer akregator kaddressbook akonadi-server abrt
	abrt-cli abrt-desktop kpat kmines kmahjongg mediawriter plasma-welcome-fedora
	fedora-release-common fedora-logos ffmpeg-free libavcodec-free mesa-va-drivers
	desktop-backgrounds-kde
)

status=0
for pkg in "${required[@]}"; do
	grep -q "^${pkg} " "${KINETIC_OUT}/packages.txt" || { echo "MISSING: ${pkg}"; status=1; }
done
for pkg in "${excluded[@]}"; do
	grep -q "^${pkg} " "${KINETIC_OUT}/packages.txt" && { echo "UNWANTED: ${pkg}"; status=1; }
done
((status == 0)) && echo "Package set: all ${#required[@]} required present, all ${#excluded[@]} exclusions absent"
exit "${status}"
