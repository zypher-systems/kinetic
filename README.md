# ZypherOS Kinetic

Kinetic is the desktop edition of **ZypherOS**, an agentic Linux distribution from Zypher Systems, based on Fedora Linux 44 with KDE Plasma.

> **Status:** 0.2.0, "Daily driver", in testing: security defaults, proven updates and rollback, and polish ([test log](docs/0.2.0-testing.md)). 0.1.0 installs cleanly in a VM ([test log](docs/build-1-testing.md)). No ISO is published yet, so build it yourself (below).

## What it is

- **Fedora 44 + KDE Plasma, mutable.** `dnf` works as usual. btrfs snapshots are the safety net: every update can be rolled back ([how](docs/recovery.md)).
- **Agents are part of the OS.** Claude Code, OpenCode, Grok Build, Codex, Gemini CLI, and Copilot CLI are ready to run and install from their official sources on first launch. VSCodium, Cursor, and Grok Bot come as standard. A system agent that helps manage the machine is planned after the first release.
- **A developer workstation out of the box.** Docker, Podman, distrobox, KVM with virt-manager, fish + starship, Ghostty, and Chromium.

See [docs/roadmap.md](docs/roadmap.md) for where Kinetic is headed and what 1.0 means, [docs/decisions.md](docs/decisions.md) for what has been decided so far and why, [docs/security.md](docs/security.md) for what Kinetic does to keep a machine safe by default, and [docs/recovery.md](docs/recovery.md) for undoing updates and recovering a machine that won't start.

## Building

On Fedora 44:

```bash
./scripts/build-rpms.sh             # no root: build Kinetic's own packages into out/repo
./scripts/check-description.sh      # no root: validate the image description and resolve packages
sudo ./scripts/build-iso.sh         # build the ISO into out/ (installs kiwi on first run; see note)
./scripts/vm.sh start               # boot it in a UEFI + Secure Boot VM, with a virtual disk to install to
```

Kinetic's own packages are published by the [Packages workflow](.github/workflows/packages.yml) whenever they change on `main`: built in a Fedora 44 container, signed with the ZypherOS key (fingerprint `098E 710A DBE3 FEE4 351B 44F4 0EE4 C89F 7AE0 182E`), and served from [zypher-systems.github.io/kinetic](https://zypher-systems.github.io/kinetic/). To publish a change to a package, bump its `Release`.

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
| `docs/roadmap.md` | Releases, and what 1.0 means |
| `docs/decisions.md` | Decisions made so far, alternatives considered, open questions |
| `docs/security.md`, `docs/recovery.md` | Security defaults; undoing updates and recovery |
| `import/devbox/` | Raw configs and wallpaper from the reference dev machine, source material for Kinetic's defaults |

## License

The code in this repository is released under the [MIT License](LICENSE), except `kiwi/fedora/`, which is Fedora's work under GPL-3.0-or-later.

The Zypher Systems and ZypherOS names, logos, and wallpapers are trademarks of Zypher Systems and are **not** covered by the MIT License.

Kinetic is based on Fedora Linux. Fedora is a trademark of Red Hat, Inc. This project is not affiliated with or endorsed by the Fedora Project or Red Hat.
