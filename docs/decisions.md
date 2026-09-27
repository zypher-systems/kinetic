# Decisions

Record of what has been decided for ZypherOS Kinetic, why, and what is still open. Last updated 2026-09-27.

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

## 0.2.0 "Daily driver": locked

Build 1 installs and works in a VM. 0.2.0 is what makes Kinetic safe to run as a main machine, judged on three things: encryption and security, proven updates and rollback, and polish. Parity with the reference machine's current setup is not a goal of this release. Tested in the VM and then on real hardware, a Lenovo ThinkPad Z16 (all AMD).

| Area | Ships in 0.2.0 |
| --- | --- |
| Firewall | Kinetic's own firewalld zone as the default. Incoming connections are refused except replies to your own traffic and: SSH, mDNS, DHCPv6, printer discovery (IPP client), Windows share browsing (Samba client), and KDE Connect. sshd is off by default, so nothing answers on the SSH port until you enable it. Changing the firewall asks for the admin password |
| Docker | Published ports listen on `127.0.0.1` unless an address is given, so `-p 8080:80` stays on the machine and `-p 0.0.0.0:8080:80` shares it. Docker's own firewall rules bypass firewalld, so this is the guard that matters. The `docker` group stays, documented as root-equivalent |
| Disk encryption | LUKS2 from the installer's "Encrypt my data", tested with Secure Boot on the Z16. Unlocking with the TPM is documented as an opt-in, with TPM + PIN recommended |
| Security record | `docs/security.md`: what is on and off by default, and why |
| Updates | A Kinetic package update and a downgrade, proven end to end from the signed repository. A Fedora update that includes a new kernel. `os-release` reports the Kinetic release (0.2.0) |
| Rollback and recovery | Proven and documented in `docs/recovery.md`: undo an update with snapper or Btrfs Assistant; boot the previous kernel from the GRUB menu; for a system that no longer boots, restore a snapshot from the Kinetic USB. No bootable snapshots |
| Polish | Plasma Setup on the Kinetic wallpaper; the boot splash checked on real hardware; dark theme consistent across Qt, GTK, Flatpak, Chromium, and VSCodium; JetBrains Mono as the system monospace font; boot time and idle memory measured on the Z16 and trimmed |
| Keyboard | Meta+Return opens Ghostty, Meta+B the browser, Meta+E the file manager, Meta+Space search. Ctrl+Alt+T stays. Existing accounts get new default shortcuts on their next login, not only new accounts |

## Later builds

- **System agent: Reeve**, including the separate Chromium profile agents drive (see [System agent](#system-agent-reeve-later))
- **NVIDIA edition**
- **Local AI**
- **Welcome app**
- **Zypher Systems' own coding agent**, to revisit later

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

### Packages and updates

Kinetic's own packages (identity, branding, defaults, agent launchers) live in `packages/` in this repository. They are built in a rootless Fedora 44 container, signed with a Zypher Systems key, and published by GitHub Actions to GitHub Pages at `zypher-systems.github.io/kinetic` whenever `main` changes. Installed systems update from there alongside Fedora. Fedora Copr was the alternative; it would have required relicensing the artwork, and packages would be signed with Copr's key rather than ours.

### Identity and branding

- `zypheros-release` replaces Fedora's release packages, following Fedora's own `generic-release` template for remixes. `os-release` says `NAME="ZypherOS"`, `ID=zypheros`, `ID_LIKE=fedora`, `PRETTY_NAME="ZypherOS Kinetic 0.1.0"`. `VERSION_ID` stays `44`, because dnf, RPM Fusion, and third-party installers use it to pick packages.
- `zypheros-logos` replaces `fedora-logos` under the same file and icon names, as Fedora's `generic-logos` does, so the installer, boot splash, Plasma launcher, and About page show ZypherOS artwork without patching anything.
- The logo is the circuit-Z mark, recreated as SVG for build 1, with a simplified version for sizes of 32 px and below. The wordmark reads ZYPHER**OS** / KINETIC in Montserrat. Sources are in `branding/`; the artwork is all rights reserved.

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

### Security defaults

- **Firewall:** Fedora's KDE edition uses its `FedoraWorkstation` zone, which accepts incoming connections on every port from 1025 to 65535, so any dev server listening on all addresses is reachable from the network. Kinetic uses its own zone instead (see [0.2.0](#020-daily-driver-locked)); open a port when you need one. firewalld chooses its defaults from `VARIANT_ID` in `os-release`, and Kinetic's (`kinetic`) is one it doesn't recognize, so build 1 already fell back to firewalld's stricter `public` zone and its password-protected policy. 0.2.0 makes that deliberate.
- **Docker:** published ports default to `127.0.0.1`. Docker writes its own firewall rules ahead of firewalld's, so without this a published port is open to the network whatever the firewall zone says. Membership in the `docker` group is equivalent to root; that is the cost of Docker working without `sudo`, and it is documented rather than hidden. Rootless Docker was the alternative: safer, but it breaks some Compose setups and tools that expect the system socket.

### Updates and recovery

- Every change Kinetic makes to a system ships in a Kinetic package, so installed systems get it from `dnf upgrade`, not only new installs. Per-user defaults (such as shortcuts) are applied once per account at login, before Plasma starts.
- Recovery uses what Fedora already has: GRUB keeps the three most recent kernels and shows its menu after a failed boot. For a system that no longer boots, the Kinetic USB has Btrfs Assistant to restore a snapshot. Bootable snapshots (openSUSE-style, via grub-btrfs) were considered and not chosen: grub-btrfs is not packaged in Fedora, and it would be one more boot component to keep working.

### System agent: Reeve (later)

The system agent will be **Reeve**, Zypher Systems' own operator agent: a command-line sysadmin agent that takes care of the machine. It is still in development and does not ship with Kinetic yet. When it is ready, it will be built from its tagged releases in Kinetic's Packages workflow, and its own before/after snapshots will be coordinated with the snapper snapshots dnf already takes. This replaces the earlier proposal of a harness-agnostic MCP server. Zypher Systems' own coding agent is deferred too.

## Open questions

- Where ISOs are published: at 3.3 GB they exceed GitHub's 2 GB limit per release file
- Local AI runtime, when it is added (Fedora's Ollama is 0.12; upstream Ollama or RamaLama are alternatives)

## Hardware notes

Checked on 2026-09-25 against Fedora 44's kernel 7.2.6 and repositories:

- **RX 9070 XT (RDNA 4):** supported by the in-kernel `amdgpu` driver and Mesa 26.2
- **H.264/H.265 hardware video:** disabled in Fedora's Mesa for patent reasons; swap in `mesa-va-drivers-freeworld` from RPM Fusion
- **MediaTek MT7927 Wi-Fi 7 + Bluetooth** (ProArt X870E): supported by the `mt7925e` and `btmtk` drivers, with firmware in `linux-firmware`. The driver is new, so test it first.
- **Board sensors:** `asus-ec-sensors` lists the ProArt X870E-Creator WiFi
- **ROCm 7.1** in Fedora 44 is built for `gfx1201` (RX 9070 XT), and Fedora's `ollama` package links against it
- **ASUS boards** usually ship with SVM (AMD virtualization) disabled in the BIOS; it must be on for KVM
- **Test laptop:** a Lenovo ThinkPad Z16 (all AMD) is the real-hardware test bed for 0.2.0: suspend and resume, battery and power profiles, Wi-Fi, the fingerprint reader, a high-DPI panel, and disk encryption with the TPM
