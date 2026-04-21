# Hardware & Framebuffer Notes

Tested target: **Raspberry Pi Zero 2W** running **Raspberry Pi OS Lite (64-bit, Bookworm)**, output via mini-HDMI, 512 MB RAM.

## Display pipeline

On RPi OS Lite there is no X server and no Wayland compositor. pygame draws directly to the kernel framebuffer at `/dev/fb0`:

```
pygame  ──►  SDL2 (SDL_VIDEODRIVER=fbdev)  ──►  /dev/fb0  ──►  HDMI
```

The systemd unit sets `SDL_VIDEODRIVER=fbdev` and `SDL_FBDEV=/dev/fb0`. The `srp` user is added to the `video`, `render`, and `tty` groups so it can open the framebuffer and suppress the console cursor.

## Resolution

By default the renderer reads `/sys/class/graphics/fb0/virtual_size` (which reflects the HDMI mode the kernel negotiated) and uses that. Override with `SRP_RESOLUTION=1280x720` in the systemd unit if you want to force a size.

For a Pi Zero 2W, `1280x720` is the sweet spot — it renders crisply, uses very little RAM, and draws in under a frame on any modern HDMI display. `1920x1080` works but uses ~6x the pixels.

### Forcing a specific HDMI mode

Edit `/boot/firmware/config.txt` (or `/boot/config.txt` on older images). For 720p:

```
hdmi_force_hotplug=1
hdmi_group=2       # DMT — PC monitor
hdmi_mode=85       # 1280x720 @ 60Hz
```

For 1080p use `hdmi_mode=82`. Reboot for changes to apply.

## KMS vs legacy framebuffer

RPi OS Bookworm uses the KMS/DRM stack by default. `/dev/fb0` still exists as a compatibility device backed by DRM — pygame's `fbdev` driver works against it in practice.

If you hit "No video device" errors, try forcing the KMS-native driver instead:

```bash
sudo systemctl edit srp-display.service
```

```ini
[Service]
Environment=SDL_VIDEODRIVER=kmsdrm
```

Then `sudo systemctl restart srp-display.service`.

## Console cursor

The blinking text cursor on tty1 is visible around pygame's render until the first blit. If it bothers you:

```bash
# Hide it at boot
echo "consoleblank=0 vt.global_cursor_default=0" | sudo tee -a /boot/firmware/cmdline.txt
```

(Keep the line a single line — don't add a newline.)

## Memory footprint

On a Pi Zero 2W running the default cycle layout at 1280×720, the process sits around 55–70 MB RSS. Each cached card surface is ~3.5 MB. The loop polls at 5 Hz and pygame's idle CPU is well under 1 %.

## Reducing SD card wear

- Logs are written to the systemd journal, which is **volatile by default** on RPi OS Lite (`Storage=auto`, empty `/var/log/journal` → RAM only). No action needed.
- If you've set `Storage=persistent` for the journal, either revert it or mount `/var/log` as tmpfs:
  ```
  tmpfs   /var/log   tmpfs   defaults,noatime,size=50M   0 0
  ```
- The app itself never writes to disk; all state lives in `/etc/srp/program.json`, which you edit by hand.

## Networking

WiFi is only used for SSH access and the occasional `git pull` via `scripts/update.sh`. The display does not need the network to operate — after initial install you could yank WiFi and it would keep cycling cards forever.

If you want the Pi to be truly offline, disable WiFi after install:

```bash
sudo nmcli radio wifi off     # or: sudo systemctl disable wpa_supplicant
```

## Audio

The Pi Zero 2W has no built-in audio out. We set `SDL_AUDIODRIVER=dummy` in the unit so pygame never tries to initialise audio — this used to hang boots with `hdmi_drive=2` on older images.

## Power and autostart

The service has `Restart=always`, so pulling the plug is safe — it just starts over on next boot. Cold-boot to first card is typically 25–35 seconds on a Zero 2W.
