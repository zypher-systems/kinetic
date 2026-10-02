# Undoing changes and recovering

ZypherOS Kinetic snapshots the system before and after every change dnf makes, so a bad update can be undone. This page covers undoing an update, booting an older kernel, and getting back a machine that no longer starts. Everything here was tested in the 0.2.0 VM; see [0.2.0 testing](0.2.0-testing.md).

## What is protected

| | In snapshots? |
| --- | --- |
| The system: programs, settings in `/etc`, the package database | Yes, before and after every `dnf` transaction, including updates from Discover (listed as "Discover (PackageKit)") |
| Your home folder, `/home` | **No.** Rolling back never touches your files, and snapshots don't back them up either; use a backup tool for that |
| Docker, Podman, and libvirt storage (`/var/lib/docker`, `/var/lib/containers/storage`, `/var/lib/libvirt/images`) | No. Separate subvolumes, so containers, images, volumes, and VM disks survive a rollback untouched |
| The boot partition, `/boot` | No; it isn't btrfs. Kinetic repairs the boot menu after a rollback (see [kernels](#rolling-back-an-update-that-installed-a-kernel)) |

Kinetic keeps the 30 most recent snapshots, plus up to 10 marked important, such as the one taken at first boot. Older ones are deleted automatically.

## Undo an update

**Use Btrfs Assistant** (in the app launcher): open the **Snapper** tab, pick the **pre** snapshot of the update you want to undo (its description is the dnf command), click **Restore**, and restart.

From a terminal, the same thing:

```bash
sudo btrfs-assistant-bin --list            # snapshots, numbered
sudo btrfs-assistant-bin --restore 42      # the "pre" snapshot of the bad update
sudo systemctl reboot
```

The whole system goes back to that moment, packages and settings together. The system you left is kept as a subvolume named `root_backup_<date>`, so a restore can itself be undone: restore that backup the same way. Once you're happy, delete it to free the space, in Btrfs Assistant's **Subvolumes** tab or with:

```bash
sudo mount -o subvolid=5 "$(findmnt -no SOURCE / | sed 's/\[.*//')" /mnt
sudo btrfs subvolume delete /mnt/root_backup_*
sudo umount /mnt
```

The update will be offered again next time. To hold back the package that caused the problem until it's fixed: `sudo dnf versionlock add <package>` (and `sudo dnf versionlock delete <package>` later).

**Don't use `snapper undochange` to undo an update.** It reverts the files an update changed, but the package database (SQLite) is written to disk later than the update's own snapshot pair, so afterwards dnf and rpm believe the update is still installed. It's fine for reverting a configuration file you edited by hand.

## Rolling back an update that installed a kernel

Kernels live on `/boot`, which snapshots don't cover. After restoring a snapshot from before a kernel update, the boot menu still starts that newer kernel, whose drivers are gone from the restored system. Kinetic detects this on the next start (`kinetic-boot-repair.service`): it makes the newest kernel that is still installed the default, removes the entries for kernels that aren't, and restarts. You'll see one extra restart with a message. That is all.

## A new kernel doesn't work

dnf keeps the three most recent kernels, and the boot menu can start any of them.

- **The menu is hidden** while boots succeed. Tap **Esc** once as the computer starts to show it; after a failed boot it appears by itself. (Pressing Esc again leaves the menu for GRUB's command line; type `normal` and press Enter to get back.)
- To show it on the next restart without racing the keyboard: `sudo grub2-editenv - set menu_show_once=1`, then restart. It waits 60 seconds.
- Pick the previous kernel. To keep starting it until the new one is fixed: `sudo grubby --set-default /boot/vmlinuz-<version>`, and hold the kernel back with `sudo dnf versionlock add kernel-core-<new version>` (delete the lock later).

## The computer doesn't start at all

Boot the ZypherOS Kinetic USB stick (choose it in the firmware's boot menu, usually F12 on Lenovo), close the Welcome Center, and:

1. **If the disk is encrypted,** open **Dolphin** and click the **Encrypted Drive** under *Devices*. Enter the disk passphrase or the recovery key (the TPM and its PIN only work when booting the installed system).
2. Open **Btrfs Assistant**. The installed system's filesystem is selected at the top.
3. Go to **Snapper → Browse/Restore** (the *New/Delete* view stays empty in the live session). Pick the snapshot to go back to, for example the **pre** snapshot of the last update, click **Restore**, and confirm.
4. Shut down, remove the USB stick, and start the computer. If the restore went back past a kernel update, expect the one extra restart from the boot menu repair.

## Individual files

Btrfs Assistant's **Browse/Restore** shows what a snapshot contains and restores single files. Snapshots are also readable by administrators at `/.snapshots/<number>/snapshot/`, for example to diff a config file: `sudo diff /.snapshots/42/snapshot/etc/fstab /etc/fstab`.
