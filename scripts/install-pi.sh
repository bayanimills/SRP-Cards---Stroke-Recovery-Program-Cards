#!/usr/bin/env bash
# Idempotent installer for the SRP display on a fresh Raspberry Pi Zero 2W
# running RPi OS Lite (Bookworm or later). Run as root via sudo.
#
#   curl -fsSL https://raw.githubusercontent.com/bayanimills/Stroke-Recovery-Program-Cards/main/scripts/install-pi.sh | sudo bash
#
# What it does:
#   1. Installs system packages: python3-venv, pygame build deps, git.
#   2. Creates the `srp` service user with video/render/tty group access.
#   3. Clones this repo into /opt/srp (or fast-forwards if it already exists).
#   4. Builds a venv at /opt/srp/venv with pygame + reportlab.
#   5. Drops /etc/srp/program.json from config/program.example.json (preserves existing).
#   6. Installs and enables the systemd unit.
#
# Safe to re-run. Exits non-zero on any failure.

set -euo pipefail

REPO_URL="${SRP_REPO_URL:-https://github.com/bayanimills/Stroke-Recovery-Program-Cards.git}"
REPO_BRANCH="${SRP_REPO_BRANCH:-main}"
INSTALL_DIR="/opt/srp"
CONFIG_DIR="/etc/srp"
CONFIG_FILE="$CONFIG_DIR/program.json"
SERVICE_USER="srp"
SERVICE_NAME="srp-display.service"

log()  { printf '\033[1;32m[srp]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[srp]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[srp]\033[0m %s\n' "$*" >&2; exit 1; }

if [[ "$(id -u)" -ne 0 ]]; then
  die "Run as root: sudo $0"
fi

log "1/6 installing apt packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y --no-install-recommends \
  git python3 python3-venv python3-pip \
  libsdl2-2.0-0 libsdl2-ttf-2.0-0 libsdl2-image-2.0-0 \
  libjpeg62-turbo libpng16-16 libfreetype6 fonts-dejavu-core \
  ca-certificates

log "2/6 creating service user '$SERVICE_USER'"
if ! id -u "$SERVICE_USER" >/dev/null 2>&1; then
  useradd --system --create-home --shell /usr/sbin/nologin "$SERVICE_USER"
fi
for grp in video render tty; do
  if getent group "$grp" >/dev/null; then
    usermod -aG "$grp" "$SERVICE_USER"
  fi
done

log "3/6 syncing repo into $INSTALL_DIR"
if [[ -d "$INSTALL_DIR/.git" ]]; then
  git -C "$INSTALL_DIR" fetch --quiet origin "$REPO_BRANCH"
  git -C "$INSTALL_DIR" reset --hard "origin/$REPO_BRANCH"
else
  rm -rf "$INSTALL_DIR"
  git clone --quiet --branch "$REPO_BRANCH" "$REPO_URL" "$INSTALL_DIR"
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

log "4/6 building venv"
if [[ ! -d "$INSTALL_DIR/venv" ]]; then
  sudo -u "$SERVICE_USER" python3 -m venv "$INSTALL_DIR/venv"
fi
sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade pip
sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install --quiet \
  -r "$INSTALL_DIR/requirements-device.txt"

log "5/6 seeding config at $CONFIG_FILE"
mkdir -p "$CONFIG_DIR"
if [[ ! -f "$CONFIG_FILE" ]]; then
  cp "$INSTALL_DIR/config/program.example.json" "$CONFIG_FILE"
  log "    wrote default program — edit $CONFIG_FILE to personalise"
else
  log "    $CONFIG_FILE already exists — left untouched"
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$CONFIG_DIR"
chmod 644 "$CONFIG_FILE"

log "6/6 installing systemd unit"
install -m 0644 "$INSTALL_DIR/systemd/$SERVICE_NAME" "/etc/systemd/system/$SERVICE_NAME"
systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"

log "done — tail logs with: journalctl -u $SERVICE_NAME -f"
log "edit program with:  sudo nano $CONFIG_FILE   (picked up within ~5s)"
