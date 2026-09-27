#!/usr/bin/env bash
# Create the ZypherOS package signing key (run once, by a person, not CI).
#
#   ./scripts/make-signing-key.sh
#
# The key lives in its own GnuPG home outside the repository, never in your
# personal keyring. The public half is written into the repository; the
# private half is left for you to store as the RPM_SIGNING_KEY GitHub secret
# and in an offline backup.
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

keydir="${ZYPHEROS_SIGNING_DIR:-${HOME}/.config/zypheros-signing}"
pubkey="${KINETIC_ROOT}/packages/kinetic-repos/keys/RPM-GPG-KEY-zypheros"

if [[ -e "${keydir}/private.asc" ]]; then
	echo "A signing key already exists in ${keydir}; refusing to overwrite it." >&2
	exit 1
fi

install -d -m 0700 "${keydir}" "${keydir}/gnupg"
export GNUPGHOME="${keydir}/gnupg"

# No passphrase: CI signs unattended. Protect the private key through the
# GitHub secret store and your offline backup instead.
gpg --batch --quiet --gen-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Key-Usage: sign
Name-Real: ZypherOS Kinetic Packages
Name-Email: zypher@zyphersystems.com
Expire-Date: 0
%commit
EOF

fingerprint="$(gpg --list-keys --with-colons | awk -F: '/^fpr:/ {print $10; exit}')"

(umask 077 && gpg --armor --export-secret-keys "${fingerprint}" > "${keydir}/private.asc")
mkdir -p "$(dirname "${pubkey}")"
gpg --armor --export "${fingerprint}" > "${pubkey}"
echo "${fingerprint}" > "${keydir}/fingerprint"

cat <<EOF

Signing key created.
  Fingerprint: ${fingerprint}
  Public key:  ${pubkey#"${KINETIC_ROOT}/"} (commit this)
  Private key: ${keydir}/private.asc

Next:
  1. Store it as a GitHub Actions secret:
       gh secret set RPM_SIGNING_KEY --repo zypher-systems/kinetic < ${keydir}/private.asc
  2. Back up ${keydir}/private.asc somewhere offline (a password manager works).
EOF
