# ZypherOS Kinetic coding agents. CLI agents (Claude Code, OpenCode, Grok
# Build, Codex, Copilot CLI, Gemini CLI) are launchers that install the agent
# for the user from its official source on first run. GUI agents (Cursor,
# Grok Bot) install from their vendors' repositories on first boot. Kinetic
# never redistributes the agents themselves.

Name:           kinetic-agents
Version:        0.1.0
Release:        1%{?dist}
Summary:        Coding agents for ZypherOS Kinetic
License:        MIT
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        agent-launcher
Source1:        firstboot-apps
Source2:        kinetic-firstboot-apps.service
Source3:        70-kinetic-agents.preset
Source4:        kinetic-agents.sh
Source5:        kinetic-agents.fish
# Anysphere's key (Cursor, Grok Bot): 380FF4BCDC34A4BD92A3565342A1772E62E492D6
# is read from keys/ next to this spec

BuildRequires:  systemd-rpm-macros

Requires:       bash
Requires:       curl
Requires:       util-linux
# Gemini CLI installs through npm
Requires:       nodejs-npm
Requires:       dnf5
%{?systemd_requires}

%global agents claude opencode grok codex copilot gemini

%description
Claude Code, OpenCode, Grok Build, Codex, GitHub Copilot CLI, and Gemini CLI
are ready to run: the first run of each installs it for the user from the
vendor's official source, and it updates itself from then on. Cursor and
Grok Bot install from their vendors' repositories on the first boot of an
installed system.


%prep


%build


%install
install -Dpm 0755 %{SOURCE0} %{buildroot}%{_libexecdir}/kinetic/agent-launcher
install -d %{buildroot}%{_libexecdir}/kinetic/agents
for agent in %{agents}; do
	ln -s ../agent-launcher %{buildroot}%{_libexecdir}/kinetic/agents/${agent}
done

install -Dpm 0755 %{SOURCE1} %{buildroot}%{_libexecdir}/kinetic/firstboot-apps
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/kinetic-firstboot-apps.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_presetdir}/70-kinetic-agents.preset
install -Dpm 0644 %{_sourcedir}/keys/RPM-GPG-KEY-anysphere %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-anysphere

install -Dpm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d/kinetic-agents.sh
install -Dpm 0644 %{SOURCE5} %{buildroot}%{_datadir}/fish/vendor_conf.d/kinetic-agents.fish

install -d %{buildroot}%{_sharedstatedir}/kinetic


%post
%systemd_post kinetic-firstboot-apps.service

%preun
%systemd_preun kinetic-firstboot-apps.service


%files
%dir %{_libexecdir}/kinetic
%{_libexecdir}/kinetic/agent-launcher
%{_libexecdir}/kinetic/agents/
%{_libexecdir}/kinetic/firstboot-apps
%{_unitdir}/kinetic-firstboot-apps.service
%{_presetdir}/70-kinetic-agents.preset
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-anysphere
%{_sysconfdir}/profile.d/kinetic-agents.sh
%{_datadir}/fish/vendor_conf.d/kinetic-agents.fish
%dir %{_sharedstatedir}/kinetic


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial agent launchers and first-boot install of Cursor and Grok Bot
