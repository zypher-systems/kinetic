# ZypherOS Kinetic snapshots: snapper snapshots of the root filesystem
# before and after every dnf transaction, set up on first boot, with
# container and VM storage on their own btrfs subvolumes so rollbacks never
# touch them, and a boot menu repair for after a snapshot restore.

Name:           kinetic-snapshots
Version:        0.2.0
Release:        1%{?dist}
Summary:        Automatic btrfs snapshots for ZypherOS Kinetic
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        snapshots-setup
Source1:        kinetic-snapshots-setup.service
Source2:        70-kinetic-snapshots.preset
Source3:        snapper.actions
Source4:        boot-repair
Source5:        kinetic-boot-repair.service

BuildRequires:  systemd-rpm-macros

Requires:       snapper
Requires:       libdnf5-plugin-actions
Requires:       btrfs-progs
Requires:       policycoreutils
Requires:       util-linux
# grub2-editenv, for the boot menu repair
Requires:       grub2-tools-minimal
Recommends:     btrfs-assistant
%{?systemd_requires}

%description
Sets up snapper for the root filesystem on first boot, takes snapshots
before and after every dnf transaction, and keeps Docker, Podman, and
libvirt image storage on separate btrfs subvolumes. Browse and restore
snapshots with btrfs-assistant. After restoring a snapshot from before a
kernel update, the boot menu is repaired on the next boot.


%prep


%build


%install
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_libexecdir}/kinetic/snapshots-setup
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/kinetic-snapshots-setup.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_presetdir}/70-kinetic-snapshots.preset
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/snapper.actions

# The boot menu repair is always on (it only acts when needed), so it is
# enabled by the package itself rather than a preset, and upgraded systems
# get it too
install -Dpm 0755 %{SOURCE4} %{buildroot}%{_libexecdir}/kinetic/boot-repair
install -Dpm 0644 %{SOURCE5} %{buildroot}%{_unitdir}/kinetic-boot-repair.service
for target in sysinit emergency; do
	install -d %{buildroot}%{_unitdir}/${target}.target.wants
	ln -s ../kinetic-boot-repair.service %{buildroot}%{_unitdir}/${target}.target.wants/
done


%post
%systemd_post kinetic-snapshots-setup.service

%preun
%systemd_preun kinetic-snapshots-setup.service


%files
%dir %{_libexecdir}/kinetic
%{_libexecdir}/kinetic/snapshots-setup
%{_unitdir}/kinetic-snapshots-setup.service
%{_libexecdir}/kinetic/boot-repair
%{_unitdir}/kinetic-boot-repair.service
%{_unitdir}/sysinit.target.wants/kinetic-boot-repair.service
%{_unitdir}/emergency.target.wants/kinetic-boot-repair.service
%{_presetdir}/70-kinetic-snapshots.preset
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/actions.d/snapper.actions


%changelog
* Sun Sep 27 2026 Zypher Systems <zypher@zyphersystems.com> - 0.2.0-1
- Fix Docker's socket not starting after the first reboot: the setup unit was
  ordered before docker.socket, an ordering cycle systemd broke by skipping it
- Repair the boot menu after restoring a snapshot from before a kernel update
- Label snapshots of updates made in Discover "Discover (PackageKit)"

* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial snapshot setup and dnf transaction snapshots
