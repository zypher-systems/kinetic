#!/usr/bin/env bash
# Assemble the signed Kinetic package repository for GitHub Pages. Run by
# CI after build-rpms.sh, with the signing key already imported into gpg.
#
#   KINETIC_SIGNING_FPR=<fingerprint> ./scripts/publish-repo.sh SITE_DIR
#
# The site keeps the last few published versions of each package so users
# can downgrade. A package whose version-release is already published is not
# replaced: bump its Release to publish a change.
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

site="${1:?usage: publish-repo.sh SITE_DIR}"
fpr="${KINETIC_SIGNING_FPR:?set KINETIC_SIGNING_FPR to the signing key fingerprint}"
base_url="${KINETIC_REPO_URL:-https://zypher-systems.github.io/kinetic}"
releasever=44
keep=3

repo_path="rpm/fedora/${releasever}"
repo="${site}/${repo_path}"
pubkey="${KINETIC_SIGNING_PUBKEY:-${KINETIC_ROOT}/packages/kinetic-repos/keys/RPM-GPG-KEY-zypheros}"

rm -rf "${site}"
mkdir -p "${repo}"

# Only ever sign with the key whose public half ships in kinetic-repos
expected="$(gpg --show-keys --with-colons "${pubkey}" | awk -F: '/^fpr:/ {print $10; exit}')"
if [[ "${fpr}" != "${expected}" ]]; then
	echo "Signing key ${fpr} does not match ${pubkey} (${expected})" >&2
	exit 1
fi

# Previously published packages, verified against the Kinetic key
if curl -fsS -o /dev/null "${base_url}/${repo_path}/repodata/repomd.xml"; then
	echo "==> Fetching published packages"
	dnf -q reposync \
		--repofrompath="kinetic-published,${base_url}/${repo_path}/" \
		--repo=kinetic-published \
		--download-path="${repo}" --norepopath
	rpmkeys --import "${pubkey}"
	rpmkeys --checksig "${repo}"/*.rpm >/dev/null
else
	echo "==> No published repository yet"
fi

echo "==> Signing new packages"
for rpm in "${KINETIC_REPO_DIR}"/*.rpm; do
	name="$(basename "${rpm}")"
	if [[ -e "${repo}/${name}" ]]; then
		echo "    ${name} is already published; keeping the published build (bump Release to replace it)"
		continue
	fi
	cp -p "${rpm}" "${repo}/"
	rpmsign --addsign --define "_gpg_name ${fpr}" "${repo}/${name}" >/dev/null
	echo "    ${name}"
done

echo "==> Keeping the newest ${keep} versions of each package"
dnf -q repomanage --old --keep "${keep}" "${repo}" | xargs -r rm -v --

createrepo_c --quiet "${repo}"
gpg --batch --yes --armor --detach-sign --local-user "${fpr}" --output "${repo}/repodata/repomd.xml.asc" "${repo}/repodata/repomd.xml"

install -pm 0644 "${pubkey}" "${site}/RPM-GPG-KEY-zypheros"
install -pm 0644 "${KINETIC_ROOT}/packages/kinetic-repos/kinetic.repo" "${site}/kinetic.repo"
cat > "${site}/index.html" <<EOF
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZypherOS Kinetic packages</title>
<style>
	body { font: 16px/1.5 system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1rem; background: #0b1220; color: #e8eef5; }
	a { color: #36a9f5; }
	code, pre { font-family: ui-monospace, monospace; }
	pre { background: #16233a; padding: 1rem; overflow-x: auto; }
</style>
<h1>ZypherOS Kinetic packages</h1>
<p>The package repository for <a href="https://github.com/zypher-systems/kinetic">ZypherOS Kinetic</a>. Kinetic systems use it already; the packages are signed with key <code>${fpr}</code>.</p>
<pre>sudo dnf config-manager addrepo --from-repofile=${base_url}/kinetic.repo</pre>
<p><a href="${repo_path}/">Browse packages</a> · <a href="RPM-GPG-KEY-zypheros">Signing key</a></p>
</html>
EOF

echo "==> Site assembled in ${site}"
find "${repo}" -maxdepth 1 -name '*.rpm' -printf '    %f\n' | sort
