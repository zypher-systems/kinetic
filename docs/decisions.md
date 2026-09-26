# Decisions

Record of what has been decided for ZypherOS Kinetic, why, and what is still open. Last updated 2026-09-25.

## Build 1 (0.1.0): locked

The first ISO: a bootable live image with an installer, tested in a VM first and then on the reference AMD machine.

| Area | Ships in build 1 |
| --- | --- |
| Base | Fedora Linux 44, KDE Plasma, mutable, Anaconda "Install to Hard Drive" |
| Identity | ZypherOS Kinetic 0.1.0 in `os-release`; circuit-Z logo (recreated as SVG) on boot splash, login screen, app launcher, installer, fastfetch; wallpaper *Zypher Systems 4K-2* on desktop, lock screen, login screen; Breeze Dark with a Zypher-blue accent |
| Shell and terminal | fish (default for new users) + starship; Ghostty as default terminal, Konsole kept as fallback; the reference machine's fish, Ghostty, and fastfetch configs with fixes applied |
| Browser | Chromium |
| CLI agents | Claude Code (stable channel), OpenCode, Grok Build, Codex, Gemini CLI, Copilot CLI: each installs from its official source the first time it is run (see [Agent installation](#agent-installation)) |
| Editors and desktop agents | VSCodium in the ISO; Grok Bot and Cursor installed at first boot from their vendors' repositories; Microsoft's VS Code repository included but disabled |
| Containers and VMs | Docker CE (buildx, compose plugin), Podman, distrobox; qemu-kvm, libvirt, swtpm, UEFI firmware, virt-manager |
| Dev tools | git, gh, glab, just, gcc/clang/cmake/ninja/make, Node.js, Python + uv, Go, Rust via rustup, Tauri build libraries (WebKitGTK 4.1, GTK3, libappindicator, librsvg, OpenSSL) |
| CLI tools | starship, zoxide, fzf, eza, bat, ripgrep, fd, btop, fastfetch, tmux, neovim |
| Desktop apps | KDE core (Dolphin, Kate, Okular, Gwenview, Spectacle, Ark, Filelight, KDE Connect, Partition Manager, Discover), LibreOffice, GIMP, Inkscape, Blender, OBS Studio; Flatseal and Gear Lever from Flathub |
| Networking | Tailscale and Syncthing, installed but off until enabled |
| Codecs and hardware | RPM Fusion free and nonfree, full ffmpeg, `mesa-va-drivers-freeworld` for H.264/H.265 hardware video, fwupd; open AMD/Intel drivers with Secure Boot on |
| Snapshots | snapper snapshots before and after every dnf transaction (dnf5 actions plugin); Docker, Podman, and libvirt storage on their own btrfs subvolumes so OS rollbacks never touch them; btrfs-assistant for browsing and restoring snapshots |
| Removed | KDE PIM and Akonadi, ABRT, Fedora's welcome tour, KDE games |
| Build tooling | kiwi, starting from Fedora's own kiwi descriptions, plus Kinetic RPMs for branding, defaults, and launchers |

## Later builds

- **System agent**, including the separate Chromium profile agents drive. Its design is decided after build 1 ships.
- **NVIDIA edition**
- **Booting into snapshots** from the boot menu
- **Local AI**
- **Welcome app**
- **Hosted package repository, signing, and CI** so installed systems receive Kinetic updates

## Decided

### Base: Fedora Linux 44, KDE Plasma

Every tool Kinetic ships already targets Fedora (Cursor, Docker CE, NVIDIA's container toolkit, and the agent harnesses), KDE Plasma is an official Fedora edition, and the six-month release cadence is current enough for development work without running a rolling base. Fedora also keeps an atomic edition possible later using the same packages, and shares its packaging and SELinux model with CentOS Stream and RHEL if ZypherOS grows a server edition.

Alternatives considered:

| Distro | Strength for this project | Why not |
| --- | --- | --- |
| openSUSE Tumbleweed | Bootable snapshots on every package change, out of the box | Smaller vendor ecosystem; rolling release is a heavy support load for a product |
| Arch / CachyOS | Newest packages, the AUR | Rolling breakage becomes our support burden; Omarchy already occupies this lane |
| Ubuntu / Kubuntu | Best vendor, NVIDIA, and CUDA support | Plasma lags, especially on LTS; Snap is built in |
| NixOS | Whole system as a reviewable config file | Prebuilt binaries need workarounds; agents are weaker at Nix |

### Mutable, not atomic (for now)

Kinetic is aimed at Docker and native desktop-app development, where builds need system `-devel` libraries and agents install packages constantly. On an atomic system all of that moves into containers. Mutable Fedora keeps `sudo dnf install` working, and the safety net comes from btrfs snapshots instead of an immutable image. An atomic (bootc) edition can be added later without changing distro.

### Naming

**ZypherOS** is the distribution. **Kinetic** is its desktop edition.

### Hardware

- The primary target is AMD. The reference machine is a Ryzen 9 9950X, Radeon RX 9070 XT, and ASUS ProArt X870E-Creator WiFi.
- The main image uses the open-source AMD and Intel graphics drivers, so Secure Boot can stay on.
- NVIDIA gets a separate edition.

### Containers and virtual machines

Docker CE comes from Docker's own repository. Podman ships alongside it without the `podman-docker` shim, which conflicts with Docker's `docker` command. distrobox keeps project toolchains separate from the host. KVM uses virt-manager as its GUI; KDE's Karton is in Fedora 44 as a 0.1 preview, to revisit later.

### Shell, terminal, browser

fish with starship, Ghostty, and Chromium. Agents drive their own separate Chromium profile and never touch the user's.

### Native desktop apps

Tauri is the planned stack (Rust with a web UI), so Rust and Tauri's build libraries ship on the host.

### Agent installation

Kinetic never redistributes proprietary agent binaries in its ISO. Everything installs from its official source, so each agent is current on day one.

**CLI agents install on first launch.** Every CLI agent ships as a small launcher. The first time it runs, it installs the agent with the vendor's official per-user installer, then hands over to it. From then on the agent updates itself, with no sudo needed. This works in the live USB session too. The first run needs internet.

| CLI agent | Official installer | Installs into |
| --- | --- | --- |
| Claude Code | `claude.ai/install.sh`, `stable` channel | `~/.local/share/claude` |
| OpenCode | `opencode.ai/install` (MIT) | `~/.opencode` |
| Grok Build | `x.ai/cli/install.sh` (source Apache-2.0) | `~/.grok` |
| Codex, Gemini CLI, Copilot CLI | Each vendor's official package | User's home directory |

**GUI apps install at first boot.** A first-boot service installs them from their vendors' signed dnf repositories and retries when the network comes up, so a machine installed offline catches up once connected. They update with `dnf upgrade`.

| App | Repository |
| --- | --- |
| Grok Bot | Anysphere's `grok-bot` repository (`downloads.cursor.com/yumrepo/grok-bot`) |
| Cursor | Anysphere's repository (`downloads.cursor.com/yumrepo`) |

### Editor: VSCodium by default

VSCodium is the MIT-licensed build of VS Code without Microsoft's telemetry or branding. Because it is open source it ships inside the ISO, from the VSCodium RPM repository. Its extensions come from Open VSX, which has the Claude Code, rust-analyzer, Tauri, Docker, Python, and clangd extensions. Microsoft keeps some extensions to its own VS Code: Dev Containers, Remote-SSH, Pylance, the C/C++ tools, and GitHub Copilot. For those, Microsoft's VS Code repository ships disabled, one command away. VSCodium also trails VS Code by a few releases.

## Proposed, not yet confirmed

- **System agent.** To be designed after build 1 ships. The starting proposal: a harness-agnostic MCP server exposing system tools (status, logs, updates and rollback, apps, services, network, displays, Plasma settings), plus an instructions file that teaches any harness how Kinetic works. The user picks their default agent at first boot. Failed services and crashed apps get a "diagnose with agent" action.

## Open questions

- Where Kinetic's own packages are hosted so installed systems get updates (Fedora COPR or GitHub)
- How to boot into snapshots on Fedora (grub-btrfs is not packaged)
- Local AI runtime, when it is added (Fedora's Ollama is 0.12; upstream Ollama or RamaLama are alternatives)

## Hardware notes

Checked on 2026-09-25 against Fedora 44's kernel 7.2.6 and repositories:

- **RX 9070 XT (RDNA 4):** supported by the in-kernel `amdgpu` driver and Mesa 26.2
- **H.264/H.265 hardware video:** disabled in Fedora's Mesa for patent reasons; swap in `mesa-va-drivers-freeworld` from RPM Fusion
- **MediaTek MT7927 Wi-Fi 7 + Bluetooth** (ProArt X870E): supported by the `mt7925e` and `btmtk` drivers, with firmware in `linux-firmware`. The driver is new, so test it first.
- **Board sensors:** `asus-ec-sensors` lists the ProArt X870E-Creator WiFi
- **ROCm 7.1** in Fedora 44 is built for `gfx1201` (RX 9070 XT), and Fedora's `ollama` package links against it
- **ASUS boards** usually ship with SVM (AMD virtualization) disabled in the BIOS; it must be on for KVM
