# Roadmap

Where ZypherOS Kinetic is headed. What has been decided, and why, is in [decisions.md](decisions.md); what each release was tested against is in its test log.

## Releases

| Release | Status |
| --- | --- |
| 0.1.0 | First ISO: base, branding, configs, agent launchers. Installed and tested in a VM ([test log](build-1-testing.md)) |
| 0.2.0 "Daily driver" | Security defaults, proven updates and rollback, polish. The current release, running on the reference desktop and laptop ([test log](0.2.0-testing.md)) |

Later, in no fixed order: the system agent (Reeve), an NVIDIA edition, local AI, and a welcome app ([decisions](decisions.md#later-builds)).

## Direction

Kinetic starts as Fedora with Zypher Systems' defaults on top. Over time, Zypher Systems' own applications replace the ones that ship with Fedora, one at a time, until the system is highly customized. KDE Plasma stays underneath; a new desktop environment is not the goal.

## In dev since 0.2.0

Checked in the VM on an ISO built from this work on 2026-10-02: boot menu, live session, and a fresh install.

- The ISO's boot menu starts ZypherOS by default; Fedora's default was the entry that checks the whole medium first, which stays in the menu
- Plasma Setup shows its welcome text over a blurred, darkened Kinetic wallpaper instead of on top of the wordmark
- No KDE Wallet wizard in the live session when unlocking a disk
- Installed systems check the Kinetic repository for updates every hour, not every six
- `build-rpms.sh` no longer needs `createrepo_c` on the host

## Polish backlog

- The installer's "Send us feedback" link points to Fedora's Anaconda forum, and its error dialog offers to file a report in Red Hat's Bugzilla. Both are built into anaconda-webui with no setting; the report sends nothing without a Bugzilla API key
- `dnf` run without `sudo` asks once per repository to import its key for Kinetic, VSCodium, Cursor, and Grok Bot, whose repository metadata is signed; answering "y" once is remembered
- VSCodium's first window closed on its very first launch in the VM and opened normally after; watch for it on real hardware
- The disk passphrase prompt names the disk by UUID ("luks-d2adcdbc-…"), as on Fedora
- Installing through Ventoy from a 2 TB SanDisk Extreme SSD was slow to start and failed while copying; the same ISO written directly to a drive, and Ventoy on a small drive in the VM, both work. Cause unconfirmed

## What 1.0 means

A polished, finished OS, with custom packages that set it apart from base Fedora.

1.0 is released when every item below is done and Zypher Systems decides to release it. It isn't the automatic next version after 0.x.

**Follows from decisions already made:**

- [ ] Nothing of Fedora's branding or first-run flow shows where a user looks: installer (including its feedback link), boot, setup, apps, and crash reporting
- [ ] Installs cleanly on the reference desktop and laptop with nothing done by hand
- [ ] Updates and rollback proven across a Fedora release upgrade (44 to 45), not only within one release
- [ ] The ISO is published for download, with checksums (where is still an [open question](decisions.md#open-questions))
- [ ] The [polish backlog](#polish-backlog) is cleared

**Proposed, not yet confirmed:**

- [ ] Reeve, Zypher Systems' system agent, packaged and set up in Kinetic
- [ ] A Kinetic welcome app for first-run setup: choosing agents, signing in, and Kinetic's own tips
- [ ] User documentation beyond security and recovery: installing, and first steps
