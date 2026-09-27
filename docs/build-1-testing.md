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
| `docker` has no socket | systemd applies presets on first boot, undoing `systemctl enable` from the image build | `70-zypheros-kinetic.preset` in `zypheros-release` enables `docker.socket` |
| Ctrl+Alt+T opens Konsole | Konsole and Ghostty both claim it; KDE's shortcut service only reads per-user config | New users get `~/.config/kglobalshortcutsrc` from `/etc/skel` (verified in the VM) |
| `/var/lib/containers` not a subvolume | It already contains files from containers-common | Subvolume at `/var/lib/containers/storage` instead |
| fish prints "mkdir: created directory" | Aliases are functions in fish, so `mkdir -pv` also applied inside fish itself | Aliases became abbreviations |
| Installer icon has text showing through | The Welcome Center draws the app name behind the icon | Installer icon is the Z on an opaque tile |

## Polish backlog

- Plasma Setup's background is Fedora's F44 wallpaper, not ZypherOS's
- The installer's "Send us feedback" link points to Fedora's Anaconda forum
- The Plymouth boot splash with the ZypherOS watermark has not been captured on screen yet
