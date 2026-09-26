# ZypherOS Kinetic

Kinetic is the desktop edition of **ZypherOS**, an agentic Linux distribution from Zypher Systems, based on Fedora Linux 44 with KDE Plasma.

> **Status:** early planning. There is no image to install yet.

## What it is

- **Fedora 44 + KDE Plasma, mutable.** `dnf` works as usual. btrfs snapshots are the safety net, so any change can be rolled back.
- **Agents are part of the OS.** Claude Code, OpenCode, Grok Build, Codex, Gemini CLI, and Copilot CLI are ready to run and install from their official sources on first launch. VSCodium, Cursor, and Grok Bot come as standard. A system agent that helps manage the machine is planned after the first release.
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
