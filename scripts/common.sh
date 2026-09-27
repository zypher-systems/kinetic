# Shared settings for Kinetic build scripts. Source, don't execute.

KINETIC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

KINETIC_VERSION="0.1.0"
KINETIC_ARCH="x86_64"
KINETIC_PROFILE="Kinetic-KDE-Desktop-Live"

# ISO 9660 volume IDs are limited to 32 characters
KINETIC_VOLID="ZypherOS-Kinetic-${KINETIC_VERSION//./_}"
KINETIC_APPID="ZypherOS-Kinetic-Live-${KINETIC_VERSION}"
KINETIC_PUBLISHER="Zypher Systems"
KINETIC_ISO_NAME="ZypherOS-Kinetic-${KINETIC_VERSION}-${KINETIC_ARCH}.iso"

KINETIC_OUT="${KINETIC_ROOT}/out"
KINETIC_DESC_DIR="${KINETIC_OUT}/description"
KINETIC_BUILD_DIR="${KINETIC_OUT}/build"
KINETIC_ISO="${KINETIC_OUT}/${KINETIC_ISO_NAME}"
KINETIC_REPO_DIR="${KINETIC_OUT}/repo"
