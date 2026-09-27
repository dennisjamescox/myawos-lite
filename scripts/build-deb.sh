#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${VERSION:-0.1.0}
ARCH=${ARCH:-all}
BUILD="$ROOT/build/deb-root"
OUTPUT="$ROOT/dist/myawos-lite_${VERSION}_${ARCH}.deb"

rm -rf "$BUILD"
mkdir -p "$BUILD/DEBIAN" "$BUILD/etc/myawos-lite" "$BUILD/lib/systemd/system"
mkdir -p "$BUILD/usr/bin" "$BUILD/usr/lib/python3/dist-packages" "$BUILD/usr/lib/udev/rules.d"
mkdir -p "$BUILD/usr/share/myawos-lite/media" "$BUILD/usr/share/doc/myawos-lite/examples"

cat > "$BUILD/DEBIAN/control" <<EOF
Package: myawos-lite
Version: $VERSION
Section: hamradio
Priority: optional
Architecture: $ARCH
Depends: python3 (>= 3.11), python3-numpy, python3-serial, alsa-utils, airspy
Maintainer: MyAWOS Project <support@myawos.com>
Description: Airspy-triggered small-airfield weather radio
 Detects microphone clicks with an Airspy receiver and keys a separate
 aviation radio through a USB relay to play local weather observations.
EOF

cp -a "$ROOT/src/myawos_lite" "$BUILD/usr/lib/python3/dist-packages/"
find "$BUILD/usr/lib/python3/dist-packages" -type d -name __pycache__ -prune -exec rm -rf {} +
cp "$ROOT/config/config.toml" "$BUILD/etc/myawos-lite/config.toml"
cp "$ROOT/packaging/myawos-lite.service" "$BUILD/lib/systemd/system/"
cp "$ROOT/packaging/99-myawos-lite.rules" "$BUILD/usr/lib/udev/rules.d/"
cp "$ROOT/examples/sample-weather.json" "$BUILD/usr/share/doc/myawos-lite/examples/"
cp "$ROOT/README.md" "$BUILD/usr/share/doc/myawos-lite/README.md"
cp -a "$ROOT/docs" "$BUILD/usr/share/doc/myawos-lite/"
cp "$ROOT"/media/*.wav "$BUILD/usr/share/myawos-lite/media/"
cp "$ROOT/packaging/postinst" "$BUILD/DEBIAN/postinst"
cp "$ROOT/packaging/prerm" "$BUILD/DEBIAN/prerm"
chmod 0755 "$BUILD/DEBIAN/postinst" "$BUILD/DEBIAN/prerm"

cat > "$BUILD/usr/bin/myawos-lite" <<'EOF'
#!/usr/bin/python3
from myawos_lite.cli import main
raise SystemExit(main())
EOF
chmod 0755 "$BUILD/usr/bin/myawos-lite"

mkdir -p "$ROOT/dist"
dpkg-deb --root-owner-group --build "$BUILD" "$OUTPUT"
echo "$OUTPUT"
