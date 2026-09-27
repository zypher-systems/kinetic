# Package repositories for ZypherOS Kinetic: Kinetic's own repository and the
# third-party repositories its standard software comes from. Signing keys
# ship in the package, verified against each vendor's published fingerprint:
#   ZypherOS      098E710ADBE3FEE4351B44F40EE4C89F7AE0182E
#   Docker CE     060A61C51B558A7F742B77AAC52FEB6B621E9F35
#   VSCodium      1302DE60231889FE1EBACADC54678CF75A278D9C
#   Microsoft     BC528686B50D79E339D3721CEB3E94ADBE1229CF
#   Copr keys come from each project's Copr page over HTTPS.
# Cursor and Grok Bot repositories are written by kinetic-agents at first
# boot, as their vendors' instructions do, because grok-bot rewrites its
# repository file on every update.

Name:           kinetic-repos
Version:        0.1.0
Release:        1%{?dist}
Summary:        Package repositories for ZypherOS Kinetic
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        kinetic.repo
Source1:        docker-ce.repo
Source2:        vscodium.repo
Source3:        vscode.repo
Source4:        copr-scottames-ghostty.repo
Source5:        copr-atim-starship.repo
# Signing keys are read from keys/ next to this spec

%description
Repository definitions and signing keys for ZypherOS Kinetic's own packages,
Docker CE, VSCodium, Microsoft Visual Studio Code (disabled by default), and
the Ghostty and starship Copr repositories.


%prep


%build


%install
repos=%{buildroot}%{_sysconfdir}/yum.repos.d
install -Dpm 0644 %{SOURCE0} ${repos}/kinetic.repo
install -Dpm 0644 %{SOURCE1} ${repos}/docker-ce.repo
install -Dpm 0644 %{SOURCE2} ${repos}/vscodium.repo
install -Dpm 0644 %{SOURCE3} ${repos}/vscode.repo
# The names dnf's copr plugin uses, so "dnf copr" can manage them
install -Dpm 0644 %{SOURCE4} "${repos}/_copr:copr.fedorainfracloud.org:scottames:ghostty.repo"
install -Dpm 0644 %{SOURCE5} "${repos}/_copr:copr.fedorainfracloud.org:atim:starship.repo"

keys=%{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -d ${keys}
install -pm 0644 %{_sourcedir}/keys/RPM-GPG-KEY-* ${keys}/


%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/kinetic.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/docker-ce.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/vscodium.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/vscode.repo
%config(noreplace) "%{_sysconfdir}/yum.repos.d/_copr:copr.fedorainfracloud.org:scottames:ghostty.repo"
%config(noreplace) "%{_sysconfdir}/yum.repos.d/_copr:copr.fedorainfracloud.org:atim:starship.repo"
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-zypheros
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-docker-ce
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-vscodium
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-microsoft
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-copr-scottames-ghostty
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-copr-atim-starship


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial repositories: Kinetic, Docker CE, VSCodium, VS Code (disabled),
  Ghostty and starship Copr
