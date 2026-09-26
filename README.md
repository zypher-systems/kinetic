# ZypherOS Kinetic

Kinetic is the desktop edition of **ZypherOS**, an agentic Linux distribution from Zypher Systems, based on Fedora Linux 44 with KDE Plasma.

> **Status:** early planning. There is no image to install yet.

## What it is

- **Fedora 44 + KDE Plasma, mutable.** `dnf` works as usual. btrfs snapshots are the safety net, so any change can be rolled back.
- **Agents are part of the OS.** The major coding agent harnesses ship ready to run, and a system agent (driven by whichever agent you choose) can manage the machine itself: read-only actions run freely, changes need your confirmation, and every change is snapshotted.
- **A developer workstation out of the box.** Docker, Podman, distrobox, KVM with virt-manager, fish + starship, Ghostty, and Chromium.

See [docs/decisions.md](docs/decisions.md) for what has been decided so far and why.

## Repository layout

| Path | Purpose |
| --- | --- |
| `docs/decisions.md` | Decisions made so far, alternatives considered, open questions |
| `import/devbox/` | Raw configs and wallpaper from the reference dev machine, source material for Kinetic's defaults |

## License

The code in this repository is released under the [MIT License](LICENSE).

The Zypher Systems and ZypherOS names, logos, and wallpapers are trademarks of Zypher Systems and are **not** covered by the MIT License.

Kinetic is based on Fedora Linux. Fedora is a trademark of Red Hat, Inc. This project is not affiliated with or endorsed by the Fedora Project or Red Hat.
