# Deploying SRP Cards to a Raspberry Pi

This turns a **Raspberry Pi Zero 2W** into a plug-and-play SRP display: power it on, cards appear on the HDMI monitor, no keyboard or mouse needed.

## What you need

- Raspberry Pi Zero 2W (or any model; Zero 2W is the tested target)
- microSD card (8 GB+), imager on your laptop
- mini-HDMI-to-HDMI cable (Pi Zero) and an HDMI display
- Power supply and a WiFi network (only used for SSH access, not the app)

## 1. Flash the SD card

Use **Raspberry Pi Imager** with **Raspberry Pi OS Lite (64-bit)**. In the imager's "advanced options" (gear icon):

- **Hostname**: `srp-display`
- **Enable SSH** → "Use password authentication" (set a password)
- **Configure WiFi**: your network
- **User**: pick any login (e.g. `pi`) — this is NOT the service user, just for SSH
- **Locale**: set your timezone

Flash and boot the Pi.

## 2. SSH in and install

From your laptop on the same network:

```bash
ssh pi@srp-display.local
```

Then run the installer — it's idempotent, so you can re-run it any time:

```bash
curl -fsSL https://raw.githubusercontent.com/bayanimills/Stroke-Recovery-Program-Cards/main/scripts/install-pi.sh | sudo bash
```

The installer:

1. Installs system packages (pygame deps, git, SDL2)
2. Creates a `srp` service user with `video`/`render`/`tty` group access
3. Clones the repo into `/opt/srp`
4. Builds a Python venv at `/opt/srp/venv`
5. Seeds `/etc/srp/program.json` from the example config
6. Installs + enables `srp-display.service` and starts it

Within a few seconds the HDMI display should wake and show the first card.

## 3. Personalise the program

SSH back in and edit the config:

```bash
sudo nano /etc/srp/program.json
```

Example:

```json
{
  "patient": "Jim",
  "dwell_minutes": 30,
  "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"]
}
```

Save and close — the display picks up the change within ~5 seconds, no restart.

### Fields

| Field | Meaning |
|-------|---------|
| `patient` | Shown in the bottom-left corner. Empty string to hide. |
| `dwell_minutes` | How long each card stays on screen before advancing. Default `30`. Must be a multiple of 15 (minimum 15): `15`, `30`, `45`, `60`, `75`, … |
| `program` | Exactly 4 entries: `"<category>_<index>"` where category is `hand`/`shoulder`/`arm`/`leg` and index is `0`, `1`, or `2`. See the exercise library below. |

The display shows one exercise at a time (large, stroke-patient-friendly),
cycling through the four in order and wrapping back to the first.

### Exercise library

| Category | Index | Exercise |
|----------|-------|----------|
| hand (★) | 0 / 1 / 2 | Stress Ball Squeeze / Finger Pinches / Water Bottle Squeeze |
| shoulder (●) | 0 / 1 / 2 | Gentle Arm Lift / Clasped Hands / Shoulder Circles |
| arm (■) | 0 / 1 / 2 | Nose Touch / Elbow Bend / Water Bottle Hold |
| leg (▲) | 0 / 1 / 2 | Knee to Chest Lift / Seated Leg Raise / Leg Up with Toes |

## 4. Operating the service

```bash
# live logs
journalctl -u srp-display.service -f

# restart after editing /etc/srp/program.json (usually unnecessary — it auto-reloads)
sudo systemctl restart srp-display.service

# stop / start / disable
sudo systemctl stop srp-display.service
sudo systemctl disable srp-display.service
```

## 5. Updating to a new release

```bash
sudo /opt/srp/scripts/update.sh
```

Pulls the latest `main`, reinstalls Python deps, and restarts the service.

## Troubleshooting

See [HARDWARE.md](HARDWARE.md) for framebuffer/HDMI details and common failure modes.

Quick checks:

```bash
# Does pygame see the framebuffer?
ls -l /dev/fb0
cat /sys/class/graphics/fb0/virtual_size

# Is the service running?
systemctl status srp-display.service

# Recent errors?
journalctl -u srp-display.service --since "5 min ago"
```
