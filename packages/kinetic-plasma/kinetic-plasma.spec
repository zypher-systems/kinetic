# ZypherOS Kinetic KDE Plasma defaults: the ZypherOS Kinetic Global Theme
# (Breeze Dark, based on Fedora's "Fedora Dark" from plasma-workspace), the
# brand accent color, the wallpaper on the desktop, lock screen, and login
# screen, Ghostty as the terminal, Chromium as the browser, and pinned apps.
# Config goes in /etc/xdg, which Plasma reads before Fedora's KDE profile.

%global lnf_id org.zypheros.kinetic.desktop

Name:           kinetic-plasma
Version:        0.1.0
Release:        1%{?dist}
Summary:        ZypherOS Kinetic KDE Plasma defaults
# The Global Theme is derived from plasma-workspace (GPL-2.0-or-later);
# the splash logo and previews are ZypherOS artwork
License:        GPL-2.0-or-later AND LicenseRef-ZypherOS-Branding
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        zypheros-mark.svg
Source1:        zypheros-kinetic.jpg
Source2:        COPYING
# The Global Theme, /etc/xdg defaults, and login screen settings are read
# from lnf/, xdg/, and plasmalogin/ next to this spec

BuildRequires:  ImageMagick
BuildRequires:  librsvg2-tools

Requires:       kinetic-backgrounds
Requires:       zypheros-logos
Requires:       plasma-workspace
Recommends:     plasma-login-manager
Recommends:     ghostty
Recommends:     chromium

%description
Makes ZypherOS Kinetic's look the default in KDE Plasma: Breeze Dark with
the ZypherOS blue accent, the ZypherOS Kinetic wallpaper on the desktop,
lock screen, and login screen, a ZypherOS boot splash, Ghostty as the
default terminal, Chromium as the default browser, and Dolphin, Chromium,
Ghostty, VSCodium, Discover, and System Settings pinned to the panel.


%prep
cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} .


%build
# Plasma splash screen logo
gzip -9 -n -c zypheros-mark.svg > plasma.svgz

# Previews shown in System Settings > Global Theme
magick zypheros-kinetic.jpg -resize 1920x1080^ -gravity center -extent 1920x1080 -strip -quality 85 fullscreenpreview.jpg
magick zypheros-kinetic.jpg -resize 800x450^ -gravity center -extent 800x450 -strip preview.png
rsvg-convert -w 160 -h 160 -o mark-160.png zypheros-mark.svg
magick -size 800x450 xc:'#0B1220' mark-160.png -gravity center -composite -strip splash.png


%install
lnf=%{buildroot}%{_datadir}/plasma/look-and-feel/%{lnf_id}
install -d ${lnf}
cp -a %{_sourcedir}/lnf/. ${lnf}/
install -pm 0644 plasma.svgz ${lnf}/contents/splash/images/plasma.svgz
install -d ${lnf}/contents/previews
install -pm 0644 fullscreenpreview.jpg preview.png splash.png ${lnf}/contents/previews/

xdg=%{buildroot}%{_sysconfdir}/xdg
install -d ${xdg}
install -pm 0644 %{_sourcedir}/xdg/kdeglobals %{_sourcedir}/xdg/kscreenlockerrc \
	%{_sourcedir}/xdg/mimeapps.list %{_sourcedir}/xdg/kde-mimeapps.list ${xdg}/

install -Dpm 0644 %{_sourcedir}/plasmalogin/50-kinetic.conf \
	%{buildroot}%{_prefix}/lib/plasmalogin/plasmalogin.conf.d/50-kinetic.conf


%files
%license COPYING
%{_datadir}/plasma/look-and-feel/%{lnf_id}/
%config(noreplace) %{_sysconfdir}/xdg/kdeglobals
%config(noreplace) %{_sysconfdir}/xdg/kscreenlockerrc
%config(noreplace) %{_sysconfdir}/xdg/mimeapps.list
%config(noreplace) %{_sysconfdir}/xdg/kde-mimeapps.list
%dir %{_prefix}/lib/plasmalogin
%dir %{_prefix}/lib/plasmalogin/plasmalogin.conf.d
%{_prefix}/lib/plasmalogin/plasmalogin.conf.d/50-kinetic.conf


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial ZypherOS Kinetic Plasma defaults and Global Theme
