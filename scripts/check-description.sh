#!/usr/bin/env bash
# Validate the kiwi description and resolve the full package list, without
# root, inside a rootless podman container. Catches missing packages and XML
# errors before a long ISO build.
#
#   ./scripts/check-description.sh            # writes out/packages.txt
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

image="localhost/kinetic-builder:44"
check_dir="${KINETIC_OUT}/description-check"

"${KINETIC_ROOT}/scripts/assemble-description.sh" "${check_dir}" >/dev/null

# kiwi's solver doesn't expand dnf variables in repository URLs; the real
# build uses dnf, which does
grep -rlE '\$(releasever|basearch)' --include='*.xml' "${check_dir}" | xargs -r sed -i \
	-e 's/\$releasever/44/g' -e "s/\\\$basearch/${KINETIC_ARCH}/g"

podman build --quiet --tag "${image}" "${KINETIC_ROOT}/containers/builder" >/dev/null

podman run --rm \
	--volume "${check_dir}:/desc:ro,Z" \
	"${image}" \
	kiwi-ng --profile="${KINETIC_PROFILE}" --type=iso --kiwi-file=Kinetic.kiwi \
		image info --description /desc --resolve-package-list \
	> "${KINETIC_OUT}/image-info.json"

python3 - "${KINETIC_OUT}/image-info.json" "${KINETIC_OUT}/packages.txt" <<'EOF'
import json, sys

raw = open(sys.argv[1]).read()
packages = json.loads(raw[raw.index("{"):])["resolved-packages"]
with open(sys.argv[2], "w") as out:
    for name in sorted(packages):
        out.write(f"{name} {packages[name]['version']} {packages[name]['arch']}\n")
listed = sum(p["status"] == "listed_in_kiwi_description" for p in packages.values())
print(f"OK: {listed} listed packages resolved ({len(packages)} with dependencies) -> {sys.argv[2]}")
print("Note: kiwi's solver skips package groups and bootstrap packages; the ISO has more.")
EOF
