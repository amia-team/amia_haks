#!/bin/bash
set -euo pipefail

# Usage: nwsync.sh <test|live|dev>
# Performs NWSync write and docker compose force-recreate for the given environment.
#
# Expected environment variables:
#   For test:  NWSYNC_PATH_TEST, TEST_SERVER_BASE, AMIA_SERVER_DIR
#   For live:  NWSYNC_PATH_LIVE, LIVE_SERVER_BASE, AMIA_SERVER_DIR
#   For dev:   NWSYNC_PATH_DEV,  DEV_SERVER_BASE,  AMIA_SERVER_DIR

ENVIRONMENT="${1:?Usage: nwsync.sh <test|live|dev>}"

if [ "${ENVIRONMENT}" = "test" ]; then
    NWSYNC_PATH="${NWSYNC_PATH_TEST:-}"
    SERVER_BASE="${TEST_SERVER_BASE:-}/test_server"
    SERVICE="test-server"
elif [ "${ENVIRONMENT}" = "live" ]; then
    NWSYNC_PATH="${NWSYNC_PATH_LIVE:-}"
    SERVER_BASE="${LIVE_SERVER_BASE:-}/server"
    SERVICE="nwserver"
elif [ "${ENVIRONMENT}" = "dev" ]; then
    NWSYNC_PATH="${NWSYNC_PATH_DEV:-}"
    SERVER_BASE="${DEV_SERVER_BASE:-}/dev_server"
    SERVICE="dev-server"
else
    echo "ERROR: Unknown environment '${ENVIRONMENT}'. Must be 'test', 'live', or 'dev'."
    exit 1
fi

if [ "${ENVIRONMENT}" = "dev" ]; then
    SERVER_DIR="${DEV_SERVER_BASE:-}"
else
    SERVER_DIR="${AMIA_SERVER_DIR:-}"
fi

# --- Determine the owner of the NWSync directory so we can run as that user ---
run_as_owner() {
    local target_dir="$1"
    shift
    local owner
    owner="$(stat -c '%U' "${target_dir}")"
    if [ "${owner}" = "$(whoami)" ]; then
        "$@"
    else
        echo "Running as '${owner}' (owner of ${target_dir})..."
        sudo -u "${owner}" "$@"
    fi
}

# --- NWSync Write ---
if [ -n "${NWSYNC_PATH}" ] && [ -n "${SERVER_BASE}" ]; then
    echo "Updating NWSync data (${ENVIRONMENT})..."
    pushd "${NWSYNC_PATH}" > /dev/null
    if [ -f ./bin/nwn_nwsync_write ] && [ -f "${SERVER_BASE}/modules/Amia.mod" ]; then
        run_as_owner "${NWSYNC_PATH}" \
            ./bin/nwn_nwsync_write --description="Amia Server Data" data/ "${SERVER_BASE}/modules/Amia.mod"
    else
        echo "NWSync binaries or module not found, skipping write..."
    fi
    popd > /dev/null
else
    echo "WARNING: NWSYNC_PATH or SERVER_BASE not set. Skipping NWSync write (${ENVIRONMENT})."
fi

# --- Docker Compose Restart ---
if [ -n "${SERVER_DIR}" ]; then
    echo "Recreating ${ENVIRONMENT} server via docker compose..."
    pushd "${SERVER_DIR}" > /dev/null
    if command -v docker &> /dev/null; then
        docker compose up -d --force-recreate "${SERVICE}"
    else
        echo "docker not found, skipping restart..."
    fi
    popd > /dev/null
else
    echo "WARNING: AMIA_SERVER_DIR not set. Skipping restart (${ENVIRONMENT})."
fi

echo "NWSync steps complete (${ENVIRONMENT})."