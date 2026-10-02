# Roadmap

Where ZypherOS Kinetic is headed. What has been decided, and why, is in [decisions.md](decisions.md); what each release was tested against is in its test log.

## Releases

| Release | Status |
| --- | --- |
| 0.1.0 | First ISO: base, branding, configs, agent launchers. Installed and tested in a VM ([test log](build-1-testing.md)) |
| 0.2.0 "Daily driver" | Security defaults, proven updates and rollback, polish. The current release, running on the reference desktop and laptop ([test log](0.2.0-testing.md)) |

Later, in no fixed order: the system agent (Reeve), an NVIDIA edition, local AI, and a welcome app ([decisions](decisions.md#later-builds)).

## What 1.0 means

A polished, finished OS, with custom packages that set it apart from base Fedora.

1.0 is released when every item below is done and Zypher Systems decides to release it. It isn't the automatic next version after 0.x.

**Follows from decisions already made:**

- [ ] Nothing of Fedora's branding or first-run flow shows where a user looks: installer (including its feedback link), boot, setup, apps, and crash reporting
- [ ] Installs cleanly on the reference desktop and laptop with nothing done by hand
- [ ] Updates and rollback proven across a Fedora release upgrade (44 to 45), not only within one release
- [ ] The ISO is published for download, with checksums (where is still an [open question](decisions.md#open-questions))
- [ ] The polish backlog in the latest test log is cleared

**Proposed, not yet confirmed:**

- [ ] Reeve, Zypher Systems' system agent, packaged and set up in Kinetic
- [ ] A Kinetic welcome app for first-run setup: choosing agents, signing in, and Kinetic's own tips
- [ ] User documentation beyond security and recovery: installing, and first steps
