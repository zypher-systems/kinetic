#!/usr/bin/env bash
# Build Kinetic's RPMs in a rootless Fedora 44 container and publish them as
# a local dnf repository in out/repo, which the ISO build uses.
#
#   ./scripts/build-rpms.sh                   # every package in packages/
#   ./scripts/build-rpms.sh zypheros-logos    # only the named packages
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

image="localhost/kinetic-builder:44"
work="${KINETIC_OUT}/rpmbuild"

cd "${KINETIC_ROOT}"

if (($#)); then
	packages=("$@")
else
	mapfile -t packages < <(find packages -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
fi

command -v createrepo_c >/dev/null || { echo "createrepo_c is required: sudo dnf install createrepo_c" >&2; exit 1; }

podman build --quiet --tag "${image}" containers/builder >/dev/null

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

podman run --rm --volume "${work}:/work:Z" "${image}" bash -euo pipefail -c '
	for dir in /work/*/; do
		pkg=$(basename "${dir}")
		echo "==> ${pkg}"
		dnf -y -q builddep "${dir}SPECS/${pkg}.spec" >/dev/null
		if ! rpmbuild -bb --define "_topdir ${dir%/}" "${dir}SPECS/${pkg}.spec" > "${dir}build.log" 2>&1; then
			tail -40 "${dir}build.log"
			echo "Build of ${pkg} failed; full log: out/rpmbuild/${pkg}/build.log" >&2
			exit 1
		fi
	done'

mkdir -p "${KINETIC_REPO_DIR}"
find "${work}" -path '*/RPMS/*' -name '*.rpm' -exec cp -p {} "${KINETIC_REPO_DIR}/" \;
createrepo_c --quiet --update "${KINETIC_REPO_DIR}"

echo "Repository: ${KINETIC_REPO_DIR}"
find "${KINETIC_REPO_DIR}" -maxdepth 1 -name '*.rpm' -printf '  %f\n' | sort
