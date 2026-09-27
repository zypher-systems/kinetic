# ZypherOS Kinetic snapshots: snapper snapshots of the root filesystem
# before and after every dnf transaction, set up on first boot, with
# container and VM storage on their own btrfs subvolumes so rollbacks never
# touch them.

Name:           kinetic-snapshots
Version:        0.1.0
Release:        1%{?dist}
Summary:        Automatic btrfs snapshots for ZypherOS Kinetic
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        snapshots-setup
Source1:        kinetic-snapshots-setup.service
Source2:        70-kinetic-snapshots.preset
Source3:        snapper.actions

BuildRequires:  systemd-rpm-macros

Requires:       snapper
Requires:       libdnf5-plugin-actions
Requires:       btrfs-progs
Requires:       policycoreutils
Requires:       util-linux
Recommends:     btrfs-assistant
%{?systemd_requires}

%description
Sets up snapper for the root filesystem on first boot, takes snapshots
before and after every dnf transaction, and keeps Docker, Podman, and
libvirt image storage on separate btrfs subvolumes. Browse and restore
snapshots with btrfs-assistant.


%prep


%build


%install
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_libexecdir}/kinetic/snapshots-setup
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/kinetic-snapshots-setup.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_presetdir}/70-kinetic-snapshots.preset
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dnf/libdnf5-plugins/actions.d/snapper.actions


%post
%systemd_post kinetic-snapshots-setup.service

%preun
%systemd_preun kinetic-snapshots-setup.service


%files
%dir %{_libexecdir}/kinetic
%{_libexecdir}/kinetic/snapshots-setup
%{_unitdir}/kinetic-snapshots-setup.service
%{_presetdir}/70-kinetic-snapshots.preset
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/actions.d/snapper.actions


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial snapshot setup and dnf transaction snapshots
