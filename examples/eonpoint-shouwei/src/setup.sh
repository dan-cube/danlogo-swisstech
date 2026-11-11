#!/usr/bin/env bash
# DanLogo toolchain setup — run once per machine.
# Installs into $DANLOGO_HOME (default ~/.danlogo) so the skill folder itself stays clean and read-only.
#   python venv : skia-pathops (boolean geometry), fonttools (SVG path pen), pillow (proof sheets)
#   node        : @resvg/resvg-js (SVG -> PNG, no system cairo needed)
set -euo pipefail
HOME_DIR="${DANLOGO_HOME:-$HOME/.danlogo}"
mkdir -p "$HOME_DIR/node"

if [ ! -x "$HOME_DIR/venv/bin/python" ]; then
  python3 -m venv "$HOME_DIR/venv"
fi
"$HOME_DIR/venv/bin/pip" install -q --upgrade pip
"$HOME_DIR/venv/bin/pip" install -q skia-pathops fonttools pillow

cd "$HOME_DIR/node"
[ -f package.json ] || npm init -y >/dev/null
npm install -q @resvg/resvg-js@2.6.2 >/dev/null

echo "DanLogo tools ready in $HOME_DIR"
echo "  python : $HOME_DIR/venv/bin/python"
echo "  render : node <skill>/examples/eonpoint-shouwei/src/render.mjs in.svg out.png [width] [--fonts]"
