# Security

What ZypherOS Kinetic does to keep a machine safe by default, and why. Kinetic is Fedora underneath, so Fedora's protections apply unchanged: SELinux, signed packages, and Secure Boot. This page covers what Kinetic sets or changes on top.

## At a glance

| | Kinetic default |
| --- | --- |
| SELinux | Enforcing, Fedora's targeted policy |
| Secure Boot | Works with it on: the image uses the open AMD and Intel drivers, with no unsigned kernel modules |
| Disk encryption | Offered by the installer ("Encrypt my data", LUKS2); recommended on laptops. [Unlocking with the TPM](#unlocking-with-the-tpm) is opt-in |
| Firewall | Kinetic's own zone: incoming connections refused except the few services below |
| Changing the firewall | Asks for an administrator password |
| Network services | None listening. sshd, Cockpit, Tailscale, and Syncthing are installed but off |
| Docker | Published ports listen on localhost only, unless you give an address |
| `docker` group | The first user is a member, so Docker works without `sudo`. This is equivalent to root (see [Docker](#docker)) |
| Packages | Signed, from Fedora, RPM Fusion, Docker, VSCodium, Anysphere (Cursor and Grok Bot), two Copr projects (Ghostty, starship), and Kinetic's own repository, whose metadata is signed too |
| Agents | Installed per user from each vendor's official source, and run with that user's permissions |

## Firewall

Kinetic's default zone is `ZypherOSKinetic`. It refuses incoming connections except replies to connections your machine made, and these services:

| Service | Why |
| --- | --- |
| SSH | So SSH works as soon as you turn sshd on. Nothing answers while sshd is off, which is the default |
| mDNS | Finding printers and other devices on the local network |
| DHCPv6 client | Getting an IPv6 address |
| IPP client | Printer discovery |
| Samba client | Browsing Windows and NAS shares |
| KDE Connect | Pairing with your phone |

Fedora's KDE edition instead uses its `FedoraWorkstation` zone, which accepts connections on every port from 1025 to 65535. That means any dev server listening on all addresses (`0.0.0.0`) is reachable by anyone on the same network, café Wi-Fi included. On Kinetic, you open a port when you mean to share something:

```bash
sudo firewall-cmd --add-port=8080/tcp        # until the next reboot
sudo firewall-cmd --permanent --add-port=8080/tcp && sudo firewall-cmd --reload   # permanently
```

`sudo firewall-cmd --list-all` shows what is open. If you've already set a different default zone yourself, Kinetic leaves it alone, including on updates.

## Docker

**Published ports stay on your machine.** Kinetic sets Docker's default bind address to `127.0.0.1` (in `/etc/docker/daemon.json`), so `docker run -p 8080:80` is reachable at `http://localhost:8080` and nowhere else. To share a port with other devices, give the address explicitly:

```bash
docker run -p 0.0.0.0:8080:80 nginx          # reachable from the network
```

In Compose, write `"0.0.0.0:8080:80"` under `ports:`. This matters because Docker writes its own firewall rules, which take effect before firewalld's: without this default, a published port is open to the network whatever the firewall zone says. Rootless Podman, which is how Podman runs by default, listens like any other program, so the firewall applies to it.

The setting applies to containers when they start, so it also covers containers created before it was set.

**The `docker` group is equivalent to root.** Anyone who can talk to the Docker daemon can start a container that mounts the whole disk. Kinetic adds the first user to `docker` so Docker works without `sudo`, the way most Docker documentation assumes. The same applies to anything running as you, including agents. To opt out:

```bash
sudo gpasswd -d "$USER" docker    # then log out and back in; use sudo docker, or Podman
```

## Disk encryption

The installer's **Encrypt my data** option encrypts the partition holding `/` and `/home` with LUKS2. The EFI and `/boot` partitions stay unencrypted, as on Fedora, so the boot loader can start. You type the passphrase at every boot, before the login screen.

Encryption protects a machine that is off. A laptop that is lost or stolen while powered down gives away nothing. Once it's unlocked, your login password and screen lock are what protect it.

### Unlocking with the TPM

Instead of the passphrase, the disk can be unlocked by the computer's TPM, which only releases the key when the machine starts with Secure Boot in the same state. This is opt-in. Choose one:

- **TPM + PIN (recommended):** at boot you type a short PIN instead of the passphrase. The TPM limits how many wrong PINs it accepts, so a short PIN is safe, and a stolen laptop still can't be unlocked without it.
- **TPM only:** the disk unlocks by itself and the computer boots straight to the login screen. The drive is useless on its own, but anyone holding the laptop gets as far as your login screen, and the data is only as safe as that.

First find the encrypted partition (the one whose `FSTYPE` is `crypto_LUKS`):

```bash
lsblk -o NAME,FSTYPE,MOUNTPOINTS
```

Then, replacing `/dev/nvme0n1p3` with that partition:

```bash
# Add a recovery key and keep it somewhere safe (a password manager, or on paper).
# Once you only type a PIN, it's easy to forget the passphrase; the recovery key
# works wherever the passphrase does.
sudo systemd-cryptenroll --recovery-key /dev/nvme0n1p3

# Enroll the TPM, bound to the Secure Boot state (PCR 7). Drop --tpm2-with-pin=yes for TPM only.
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 --tpm2-with-pin=yes /dev/nvme0n1p3

# Use the TPM at boot, and rebuild the boot image with TPM support
sudo sed -i '/^luks-/ s/$/,tpm2-device=auto/' /etc/crypttab
sudo dracut -f
```

`sudo systemd-cryptenroll /dev/nvme0n1p3` lists what can unlock the disk: your passphrase, the recovery key, and the TPM. Your passphrase keeps working, at the boot prompt and from the Kinetic USB stick.

If the Secure Boot state changes (Secure Boot turned off, or a firmware or Secure Boot database update), the TPM refuses and the boot asks for the passphrase instead. Enroll the TPM again with the same command plus `--wipe-slot=tpm2`. To stop using the TPM: `sudo systemd-cryptenroll --wipe-slot=tpm2 /dev/nvme0n1p3`, remove `,tpm2-device=auto` from `/etc/crypttab`, and run `sudo dracut -f`.

## What's off until you turn it on

| Service | To turn it on |
| --- | --- |
| SSH server | `sudo systemctl enable --now sshd` |
| Cockpit (web admin) | `sudo systemctl enable --now cockpit.socket`, then `sudo firewall-cmd --permanent --add-service=cockpit && sudo firewall-cmd --reload` to reach it from another machine |
| Tailscale | `sudo systemctl enable --now tailscaled`, then `sudo tailscale up` |
| Syncthing | `systemctl --user enable --now syncthing` |

## Updates and trust

Kinetic's own packages come from `zypher-systems.github.io/kinetic`, signed with the ZypherOS key (fingerprint `098E 710A DBE3 FEE4 351B 44F4 0EE4 C89F 7AE0 182E`), and dnf checks the repository metadata's signature too. Fedora's packages and updates come from Fedora as usual. Every update is snapshotted before and after, so it can be undone ([recovery](recovery.md)).

## Agents

The CLI agents (Claude Code, OpenCode, Grok Build, Codex, Gemini CLI, Copilot CLI) are not in the image. The first time you run one, Kinetic's launcher downloads it over HTTPS from its vendor's official installer into your home directory, and from then on it updates itself. You are trusting each vendor, as you would installing it yourself.

An agent runs as you, with your permissions. It can read your files, use your SSH keys, run `docker` (root-equivalent, above), and run `sudo` if you type your password for it. Decide which agents you let run commands without asking, and on what.
