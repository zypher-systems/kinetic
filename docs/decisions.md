# Decisions

Record of what has been decided for ZypherOS Kinetic, why, and what is still open. Last updated 2026-09-25.

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

- **Docker CE** from Docker's own repository, with buildx and the compose plugin
- **Podman**, alongside Docker; no `podman-docker` shim, since it conflicts with Docker's `docker` command
- **distrobox**, for keeping project toolchains separate from the host
- **KVM:** qemu-kvm, libvirt, swtpm, and UEFI firmware, with **virt-manager** as the GUI. KDE's Karton is in Fedora 44 as a 0.1 preview; revisit later.

### Shell, terminal, browser

- **fish** with **starship** as the default shell
- **Ghostty** as the default terminal
- **Chromium** as the default browser. Agents drive their own separate Chromium profile and never touch the user's.

## Proposed, not yet confirmed

- **Agent harnesses.** Claude Code, OpenCode, Grok, Codex, Gemini CLI, and Copilot CLI ship as launchers that install from the official source on first run. Cursor and VS Code come from their vendors' RPM repositories.
- **System agent.** A harness-agnostic MCP server exposing system tools (status, logs, updates and rollback, apps, services, network, displays, Plasma settings), plus an instructions file that teaches any harness how Kinetic works. The user picks their default agent at first boot. Failed services and crashed apps get a "diagnose with agent" action.
- **Snapshots.** snapper takes a snapshot before and after every dnf transaction, via dnf5's actions plugin. Docker, Podman, and libvirt storage live on separate btrfs subvolumes so an OS rollback never touches them.
- **Removed for speed.** KDE PIM and Akonadi, KDE games, ABRT (replaced by agent crash diagnosis), Fedora's welcome tour, and Baloo file-content indexing.
- **Build tooling.** Fedora's own kiwi descriptions plus a Kinetic RPM repository, rather than livemedia-creator.

## Open questions

- Which stack native desktop apps are built with (Tauri, Electron, Qt, Flutter), which decides the thick-app dev bundle
- Office and creative apps (LibreOffice, GIMP, Inkscape, Blender, OBS): default install or an optional extras bundle
- Local AI: include by default, and which runtime (Fedora's Ollama is 0.12; upstream Ollama or RamaLama are alternatives)
- Tailscale and Syncthing
- Wallpapers: one default or a Zypher Systems pack
- Booting into a snapshot from the boot menu, which Fedora does not provide out of the box (grub-btrfs is not packaged)

## Hardware notes

Checked on 2026-09-25 against Fedora 44's kernel 7.2.6 and repositories:

- **RX 9070 XT (RDNA 4):** supported by the in-kernel `amdgpu` driver and Mesa 26.2
- **H.264/H.265 hardware video:** disabled in Fedora's Mesa for patent reasons; swap in `mesa-va-drivers-freeworld` from RPM Fusion
- **MediaTek MT7927 Wi-Fi 7 + Bluetooth** (ProArt X870E): supported by the `mt7925e` and `btmtk` drivers, with firmware in `linux-firmware`. The driver is new, so test it first.
- **Board sensors:** `asus-ec-sensors` lists the ProArt X870E-Creator WiFi
- **ROCm 7.1** in Fedora 44 is built for `gfx1201` (RX 9070 XT), and Fedora's `ollama` package links against it
- **ASUS boards** usually ship with SVM (AMD virtualization) disabled in the BIOS; it must be on for KVM
