# ZypherOS release identity, replacing fedora-release-common,
# fedora-release-kde-desktop, and fedora-release-identity-kde-desktop.
# Modeled on Fedora's fedora-release 44 (common and KDE Plasma Desktop parts)
# and generic-release, Fedora's template for remixes. The systemd presets,
# dnf defaults, and dnf protected list are Fedora's, unchanged.

%global dist_version    44
%global kinetic_version 0.1.0
# Fedora Linux 44 end of life; ZypherOS Kinetic tracks its base
%global eol_date        2027-05-19

Name:           zypheros-release
Version:        %{dist_version}
Release:        1%{?dist}
Summary:        ZypherOS Kinetic release files
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        LICENSE
Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
Source4:        90-default-user.preset
Source5:        80-kde-desktop.preset
Source6:        81-desktop.preset
Source7:        20-fedora-defaults.conf
Source8:        plasma-desktop.conf
Source9:        zypheros-kinetic.conf

# dnf5 derives $releasever from the package that provides system-release
Provides:       system-release
Provides:       system-release(%{version})
Provides:       zypheros-release-identity = %{version}-%{release}

# Fedora's package repositories stay; only the identity changes
Requires:       fedora-repos(%{version})

Conflicts:      fedora-release
Conflicts:      fedora-release-common
Conflicts:      fedora-release-identity
Conflicts:      generic-release
Conflicts:      generic-release-common

%description
Release files that identify the system as ZypherOS Kinetic, the desktop
edition of ZypherOS, based on Fedora Linux %{dist_version}: os-release, issue,
rpm dist macros, Fedora's systemd presets for KDE Plasma desktops, and the
installer profile.


%prep


%build


%install
install -d %{buildroot}%{_prefix}/lib %{buildroot}%{_sysconfdir}

echo "ZypherOS release %{dist_version} (Kinetic)" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:zyphersystems:zypheros:%{kinetic_version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Many tools read these Fedora-named paths to detect the distribution
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# VERSION_ID stays at the Fedora base version: dnf, RPM Fusion, and
# third-party installers use it (with ID_LIKE=fedora) to pick packages.
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="ZypherOS"
VERSION="%{kinetic_version} (Kinetic)"
RELEASE_TYPE=stable
ID=zypheros
ID_LIKE=fedora
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PRETTY_NAME="ZypherOS Kinetic %{kinetic_version}"
ANSI_COLOR="0;38;2;54;169;245"
LOGO=zypheros-logo-icon
CPE_NAME="cpe:/o:zyphersystems:zypheros:%{kinetic_version}"
DEFAULT_HOSTNAME="zypheros"
HOME_URL="https://zyphersystems.com/"
DOCUMENTATION_URL="https://github.com/zypher-systems/kinetic"
SUPPORT_URL="https://github.com/zypher-systems/kinetic/issues"
BUG_REPORT_URL="https://github.com/zypher-systems/kinetic/issues"
SUPPORT_END=%{eol_date}
VARIANT="Kinetic"
VARIANT_ID=kinetic
ZYPHEROS_VERSION=%{kinetic_version}
EOF
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

install -d %{buildroot}%{_sysconfdir}/issue.d

# Same dist macros as Fedora, so packages built here match Fedora's
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%distcore            .fc%%{fedora}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?with_bootstrap:%%{__bootstrap}}%%{?buildrelease:+build%%{buildrelease}}
%%dist_vendor         ZypherOS
%%dist_name           ZypherOS
%%dist_purl_namespace fedora
%%dist_home_url       https://zyphersystems.com/
%%dist_bug_report_url https://github.com/zypher-systems/kinetic/issues
%%dist_debuginfod_url ima:enforcing https://debuginfod.fedoraproject.org/ ima:ignore
EOF

install -Dm0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE5} %{SOURCE6} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE4} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
install -Dm0644 %{SOURCE3} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
install -Dm0644 %{SOURCE7} %{buildroot}%{_datadir}/dnf5/libdnf.conf.d/20-zypheros-defaults.conf
install -Dm0644 %{SOURCE8} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/

# Installer settings, inherited from Fedora KDE's Anaconda profile
install -Dm0644 %{SOURCE9} -t %{buildroot}%{_sysconfdir}/anaconda/profile.d/

install -d licenses
install -pm 0644 %{SOURCE0} licenses/LICENSE


%files
%license licenses/LICENSE
%{_prefix}/lib/os-release
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/80-kde-desktop.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%{_datadir}/dnf5/libdnf.conf.d/20-zypheros-defaults.conf
%config(noreplace) %{_sysconfdir}/dnf/protected.d/plasma-desktop.conf
%dir %{_sysconfdir}/anaconda
%dir %{_sysconfdir}/anaconda/profile.d
%{_sysconfdir}/anaconda/profile.d/zypheros-kinetic.conf


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 44-1
- Initial ZypherOS Kinetic 0.1.0 release package, from fedora-release 44-18
