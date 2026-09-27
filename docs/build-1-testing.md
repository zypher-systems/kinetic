# Build 1 testing

VM testing of ZypherOS Kinetic 0.1.0 with `scripts/vm.sh` (UEFI, Secure Boot on, 8 GB RAM, 64 GB virtual disk).

## First full install (ISO of 2026-09-27)

Verified working:

- Boot under Secure Boot; GRUB, live session, `mokutil` reports Secure Boot enabled
- Branding: wallpaper on desktop, lock screen, and login screen; Z mark on the launcher; Welcome Center, installer, Plasma Setup, and TTY all say ZypherOS Kinetic 0.1.0
- Installer: Kinetic's Anaconda profile applies (btrfs `/` and `/home`, `fedora` EFI directory, accounts left to Plasma Setup)
- Plasma Setup creates the user in `wheel`, `docker`, and `libvirt`; hostname defaults to `zypheros`
- First boot: snapper baseline snapshot, pre/post snapshots around the first-boot dnf transaction, `var/lib/docker` and `var/lib/libvirt/images` as subvolumes; Cursor, Grok Bot, Flatseal, and Gear Lever installed
- Ghostty with fish, the Zypher greeting, and starship; fastfetch with the ZypherOS logo
- `claude` launcher installs Claude Code (stable channel) on first run and hands over to it

Found and fixed for the next build:

| Problem | Cause | Fix |
| --- | --- | --- |
| Installed system boots to a GRUB menu with no ZypherOS entry | `grub2-mkconfig` recorded `blsdir` as the btrfs build host's path of the image root | `kiwi/config.sh` unsets `blsdir`; an Anaconda post-script in `zypheros-release` does too |
| `docker` has no socket | Thought to be systemd reapplying presets on first boot; the second install showed the real cause (below) | `70-zypheros-kinetic.preset` in `zypheros-release`; not enough on its own, see below |
| Ctrl+Alt+T opens Konsole | Konsole and Ghostty both claim it; KDE's shortcut service only reads per-user config | New users get `~/.config/kglobalshortcutsrc` from `/etc/skel` (verified in the VM) |
| `/var/lib/containers` not a subvolume | It already contains files from containers-common | Subvolume at `/var/lib/containers/storage` instead |
| fish prints "mkdir: created directory" | Aliases are functions in fish, so `mkdir -pv` also applied inside fish itself | Aliases became abbreviations |
| Installer icon has text showing through | The Welcome Center draws the app name behind the icon | Installer icon is the Z on an opaque tile |

## Second install (ISO of 2026-09-27, afternoon)

Confirmed fixed: the installed system boots straight into ZypherOS (GRUB environment has no `blsdir`); Ctrl+Alt+T opens Ghostty for a new user; fish prints nothing extra; the installer icon is an opaque tile.

Still broken, fixed for the next build:

| Problem | Cause | Fix |
| --- | --- | --- |
| `docker.socket` still disabled | Live installs keep the image's unit states, and the installer assigns a machine ID, so systemd never applies presets on first boot; docker-ce doesn't apply presets to its socket either | `kinetic-snapshots-setup` enables and starts `docker.socket` on first boot. Verified by hand in the VM: `docker run hello-world` works for a `docker` group member |
| `/var/lib/containers/storage` not a subvolume | `systemd-tmpfiles` creates an empty `tmp` inside it at boot | Directories holding only empty directories count as empty; `systemd-tmpfiles` recreates them inside the new subvolume |

## Third install (ISO of 2026-09-27, 11:17)

Everything in the build 1 spec passed, with nothing done by hand: boots straight into ZypherOS; Plasma Setup user in `wheel`, `docker`, and `libvirt`; Ctrl+Alt+T opens Ghostty with fish; `docker.socket` enabled and active, and `docker run hello-world` works for the user; `var/lib/docker`, `var/lib/containers/storage`, and `var/lib/libvirt/images` are subvolumes; baseline and dnf pre/post snapshots exist; Cursor, Grok Bot, Flatseal, and Gear Lever installed on first boot.

Next: real hardware (Ryzen 9 9950X, Radeon RX 9070 XT, ASUS ProArt X870E-Creator WiFi), especially Wi-Fi 7 and Bluetooth on the MT7927.

## Polish backlog

- Plasma Setup's background is Fedora's F44 wallpaper, not ZypherOS's
- The installer's "Send us feedback" link points to Fedora's Anaconda forum; it is built into anaconda-webui, not configurable
- The Plymouth boot splash with the ZypherOS watermark has not been captured on screen yet (the VM boots too fast)
