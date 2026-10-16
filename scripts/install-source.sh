#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ "$(id -u)" -ne 0 ]; then
    echo "Run this installer with sudo." >&2
    exit 1
fi

apt-get update
apt-get install -y python3 python3-numpy python3-serial alsa-utils airspy
VERSION=${VERSION:-0.1.1} "$ROOT/scripts/build-deb.sh"
dpkg -i "$ROOT/dist/myawos-lite_${VERSION:-0.1.1}_all.deb"
