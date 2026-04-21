#!/usr/bin/env bash
# Pull the latest code and restart the display.
# Run on the Pi:   sudo /opt/srp/scripts/update.sh

set -euo pipefail

INSTALL_DIR="/opt/srp"
SERVICE_NAME="srp-display.service"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root: sudo $0" >&2
  exit 1
fi

cd "$INSTALL_DIR"
git fetch --quiet origin
git reset --hard "origin/$(git rev-parse --abbrev-ref HEAD)"
sudo -u srp "$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade \
  -r "$INSTALL_DIR/requirements-device.txt"
systemctl restart "$SERVICE_NAME"
systemctl status "$SERVICE_NAME" --no-pager --lines=5
