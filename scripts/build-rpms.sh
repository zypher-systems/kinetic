#!/usr/bin/env bash
# Build Kinetic's RPMs in a rootless Fedora 44 container and publish them as
# a local dnf repository in out/repo, which the ISO build uses.
#
#   ./scripts/build-rpms.sh                   # every package in packages/
#   ./scripts/build-rpms.sh zypheros-logos    # only the named packages
#   ./scripts/build-rpms.sh --no-container    # build directly, as root in a
#                                             # Fedora 44 container (CI)
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

image="localhost/kinetic-builder:44"
work="${KINETIC_OUT}/rpmbuild"

use_container=1
if [[ "${1:-}" == "--no-container" ]]; then
	use_container=0
	shift
fi

cd "${KINETIC_ROOT}"

if (($#)); then
	packages=("$@")
else
	mapfile -t packages < <(find packages -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
fi

if ! ((use_container)); then
	command -v createrepo_c >/dev/null || { echo "createrepo_c is required: sudo dnf install createrepo_c" >&2; exit 1; }
fi

# Stage each package: its spec, its own files, and the shared branding sources
rm -rf "${work}"
for pkg in "${packages[@]}"; do
	spec="packages/${pkg}/${pkg}.spec"
	[[ -f "${spec}" ]] || { echo "No spec at ${spec}" >&2; exit 1; }
	mkdir -p "${work}/${pkg}/SPECS" "${work}/${pkg}/SOURCES"
	cp -p "${spec}" "${work}/${pkg}/SPECS/"
	# Package files keep their layout; branding sources are flattened in
	cp -a "packages/${pkg}/." "${work}/${pkg}/SOURCES/"
	rm -f "${work}/${pkg}/SOURCES/${pkg}.spec"
	find branding -type f ! -name README.md -exec cp -p {} "${work}/${pkg}/SOURCES/" \;
done

# Builds every staged package; the staging directory is $1
build_loop='
	for dir in "$1"/*/; do
		pkg=$(basename "${dir}")
		echo "==> ${pkg}"
		dnf -y -q builddep "${dir}SPECS/${pkg}.spec" >/dev/null
		if ! rpmbuild -bb --define "_topdir ${dir%/}" "${dir}SPECS/${pkg}.spec" > "${dir}build.log" 2>&1; then
			tail -40 "${dir}build.log"
			echo "Build of ${pkg} failed; full log: out/rpmbuild/${pkg}/build.log" >&2
			exit 1
		fi
	done'

if ((use_container)); then
	podman build --quiet --tag "${image}" containers/builder >/dev/null
	podman run --rm --volume "${work}:/work:Z" "${image}" bash -euo pipefail -c "${build_loop}" _ /work
else
	bash -euo pipefail -c "${build_loop}" _ "${work}"
fi

mkdir -p "${KINETIC_REPO_DIR}"
find "${work}" -path '*/RPMS/*' -name '*.rpm' -exec cp -p {} "${KINETIC_REPO_DIR}/" \;
if ((use_container)); then
	podman run --rm --volume "${KINETIC_REPO_DIR}:/repo:Z" "${image}" createrepo_c --quiet --update /repo
else
	createrepo_c --quiet --update "${KINETIC_REPO_DIR}"
fi

echo "Repository: ${KINETIC_REPO_DIR}"
find "${KINETIC_REPO_DIR}" -maxdepth 1 -name '*.rpm' -printf '  %f\n' | sort
