#!/bin/bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SOURCE_DIR/.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/build"
APP_BUNDLE="$OUTPUT_DIR/Murphy Voice Studio.app"

mkdir -p "$APP_BUNDLE/Contents/MacOS" "$APP_BUNDLE/Contents/Resources"
cp "$SOURCE_DIR/Info.plist" "$APP_BUNDLE/Contents/Info.plist"
cp "$SOURCE_DIR/launcher.sh" "$APP_BUNDLE/Contents/MacOS/launcher"
cp "$SOURCE_DIR/resources/AppIcon.icns" "$APP_BUNDLE/Contents/Resources/AppIcon.icns"
chmod +x "$APP_BUNDLE/Contents/MacOS/launcher"
/usr/bin/codesign --force --sign - "$APP_BUNDLE"
printf 'Built: %s\n' "$APP_BUNDLE"
