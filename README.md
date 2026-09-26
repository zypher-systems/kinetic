# ZypherOS Kinetic

Kinetic is the desktop edition of **ZypherOS**, an agentic Linux distribution from Zypher Systems, based on Fedora Linux 44 with KDE Plasma.

> **Status:** early planning. There is no image to install yet.

## What it is

- **Fedora 44 + KDE Plasma, mutable.** `dnf` works as usual. btrfs snapshots are the safety net, so any change can be rolled back.
- **Agents are part of the OS.** Claude Code, OpenCode, Grok Build, Codex, Gemini CLI, and Copilot CLI are ready to run and install from their official sources on first launch. VSCodium, Cursor, and Grok Bot come as standard. A system agent that helps manage the machine is planned after the first release.
- **A developer workstation out of the box.** Docker, Podman, distrobox, KVM with virt-manager, fish + starship, Ghostty, and Chromium.

See [docs/decisions.md](docs/decisions.md) for what has been decided so far and why.

## Building

On Fedora 44:

```bash
./scripts/build-rpms.sh             # no root: build Kinetic's own packages into out/repo
./scripts/check-description.sh      # no root: validate the image description and resolve packages
sudo ./scripts/build-iso.sh         # build the ISO into out/ (installs kiwi on first run; see note)
./scripts/vm.sh start               # boot it in a UEFI + Secure Boot VM, with a virtual disk to install to
```

**SELinux note:** kiwi's SELinux policy (`kiwi-selinux`) blocks rpm 6 from running package user/group scriptlets during the build. `build-iso.sh` makes only kiwi's `kiwi_t` domain permissive while it runs and restores it afterwards, even if the build fails. The rest of the system stays enforcing.

## Repository layout

| Path | Purpose |
| --- | --- |
| `kiwi/Kinetic.kiwi`, `kiwi/kinetic/` | Kinetic's kiwi image description |
| `kiwi/fedora/` | Fedora's kiwi descriptions, vendored unmodified (GPL-3.0; see its `SNAPSHOT`) |
| `kiwi/config.sh` | Runs inside the image during the build: Fedora's config, then Kinetic's |
| `packages/` | Kinetic's own RPMs: identity, logos, wallpaper, defaults |
| `branding/` | Source artwork (all rights reserved; see `branding/COPYING`) |
| `scripts/` | Build, check, signing-key, and VM test scripts |
| `containers/builder/` | Rootless container used by `check-description.sh` |
| `docs/decisions.md` | Decisions made so far, alternatives considered, open questions |
| `import/devbox/` | Raw configs and wallpaper from the reference dev machine, source material for Kinetic's defaults |

## License

The code in this repository is released under the [MIT License](LICENSE), except `kiwi/fedora/`, which is Fedora's work under GPL-3.0-or-later.

The Zypher Systems and ZypherOS names, logos, and wallpapers are trademarks of Zypher Systems and are **not** covered by the MIT License.

Kinetic is based on Fedora Linux. Fedora is a trademark of Red Hat, Inc. This project is not affiliated with or endorsed by the Fedora Project or Red Hat.
