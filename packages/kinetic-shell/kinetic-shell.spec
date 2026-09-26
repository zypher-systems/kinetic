# ZypherOS Kinetic terminal defaults: the Zypher Systems fish configuration
# for every user, fastfetch with the ZypherOS logo, and Ghostty defaults for
# new accounts. The login shell stays bash so the Plasma session environment
# (built from /etc/profile.d) is complete; terminals start fish.

Name:           kinetic-shell
Version:        0.1.0
Release:        1%{?dist}
Summary:        ZypherOS Kinetic terminal defaults (fish, fastfetch, Ghostty)
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Requires:       fish
Requires:       starship
Requires:       zoxide
Requires:       eza
Requires:       bat
Requires:       fastfetch
Requires:       fzf
Requires:       ripgrep
Requires:       fd-find
Requires:       btop
Recommends:     ghostty

%description
Default terminal experience for ZypherOS Kinetic: fish with the Zypher
Systems colors, aliases, greeting, starship prompt, and zoxide; helper
functions (extract, update, netinfo, weather); fastfetch showing the
ZypherOS logo; and Ghostty defaults with the Carbonfox theme for new users.


%prep


%build


%install
fish=%{buildroot}%{_datadir}/fish
install -Dpm 0644 %{_sourcedir}/fish/kinetic.fish ${fish}/vendor_conf.d/kinetic.fish
install -d ${fish}/vendor_functions.d
install -pm 0644 %{_sourcedir}/fish/functions/*.fish ${fish}/vendor_functions.d/

install -Dpm 0644 %{_sourcedir}/fastfetch/config.jsonc %{buildroot}%{_sysconfdir}/xdg/fastfetch/config.jsonc
install -Dpm 0644 %{_sourcedir}/fastfetch/zypheros.txt %{buildroot}%{_datadir}/kinetic/fastfetch/zypheros.txt

install -Dpm 0644 %{_sourcedir}/ghostty/config.ghostty %{buildroot}%{_sysconfdir}/skel/.config/ghostty/config.ghostty


%files
%{_datadir}/fish/vendor_conf.d/kinetic.fish
%{_datadir}/fish/vendor_functions.d/*.fish
%dir %{_sysconfdir}/xdg/fastfetch
%config(noreplace) %{_sysconfdir}/xdg/fastfetch/config.jsonc
%dir %{_datadir}/kinetic
%{_datadir}/kinetic/fastfetch/
%dir %{_sysconfdir}/skel/.config
%dir %{_sysconfdir}/skel/.config/ghostty
%config(noreplace) %{_sysconfdir}/skel/.config/ghostty/config.ghostty


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial terminal defaults from the Zypher Systems fish, fastfetch, and
  Ghostty configurations
