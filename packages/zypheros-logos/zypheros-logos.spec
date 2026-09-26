# ZypherOS logos, replacing fedora-logos. Follows Fedora's generic-logos
# pattern: the same file and icon names that the installer, boot splash,
# Plasma, and Cockpit look up, carrying ZypherOS artwork. PNGs are rendered
# from the SVG sources at build time.

Name:           zypheros-logos
Version:        0.1.0
Release:        1%{?dist}
Summary:        ZypherOS logos and branding images
License:        LicenseRef-ZypherOS-Branding
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        zypheros-mark.svg
Source1:        zypheros-mark-small.svg
Source2:        zypheros-kinetic-lockup-dark.svg
Source3:        zypheros-kinetic-lockup-light.svg
Source4:        COPYING

BuildRequires:  librsvg2-tools
BuildRequires:  ImageMagick

Provides:       system-logos = %{version}-%{release}
Conflicts:      fedora-logos
Conflicts:      generic-logos

%description
The ZypherOS circuit-Z mark and ZypherOS Kinetic wordmark, installed under
the names the installer, boot splash, KDE Plasma, and Cockpit expect.


%prep
cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .


%build
mark=zypheros-mark.svg
small=zypheros-mark-small.svg
dark=zypheros-kinetic-lockup-dark.svg
light=zypheros-kinetic-lockup-light.svg

mkdir -p out
# Square icons: the simplified mark up to 32 px, the full mark above
for size in 16 22 24 32 36 48 64 96 128 256; do
	src=${mark}
	[ ${size} -le 32 ] && src=${small}
	rsvg-convert -w ${size} -h ${size} -o out/logo-${size}.png ${src}
	rsvg-convert -w ${size} -h ${size} -o out/start-here-${size}.png ${small}
done
rsvg-convert -w 252 -h 252 -o out/mark-252.png ${mark}
rsvg-convert -w 16 -h 16 -o out/favicon.png ${small}

# Wordmark lockups at Fedora's image heights (width follows the aspect ratio)
rsvg-convert -h 164 -o out/lockup-light-164.png ${light}
rsvg-convert -h 47 -o out/lockup-light-47.png ${light}
rsvg-convert -h 80 -o out/lockup-light-80.png ${light}
rsvg-convert -h 80 -o out/lockup-dark-80.png ${dark}
rsvg-convert -h 43 -o out/lockup-dark-43.png ${dark}
rsvg-convert -h 64 -o out/lockup-dark-64.png ${dark}
rsvg-convert -h 69 -o out/lockup-dark-69.png ${dark}
rsvg-convert -h 36 -o out/lockup-dark-36.png ${dark}

# GTK installer backgrounds, in the brand's dark slate
magick -size 406x767 gradient:'#16233A-#0B1220' out/sidebar-bg.png
magick -size 1040x132 xc:'#0B1220' out/topbar-bg.png


%install
icons=%{buildroot}%{_datadir}/icons/hicolor
for size in 16 22 24 32 36 48 64 96 128 256; do
	install -Dpm 0644 out/logo-${size}.png ${icons}/${size}x${size}/apps/zypheros-logo-icon.png
	install -Dpm 0644 out/logo-${size}.png ${icons}/${size}x${size}/apps/fedora-logo-icon.png
	install -Dpm 0644 out/start-here-${size}.png ${icons}/${size}x${size}/places/start-here.png
done
install -Dpm 0644 zypheros-mark.svg ${icons}/scalable/apps/zypheros-logo-icon.svg
install -Dpm 0644 zypheros-mark.svg ${icons}/scalable/apps/fedora-logo-icon.svg
install -Dpm 0644 zypheros-mark-small.svg ${icons}/scalable/places/start-here.svg
install -Dpm 0644 zypheros-mark-small.svg ${icons}/scalable/apps/start-here.svg
# The live session's "Install to Hard Drive" icon
install -Dpm 0644 zypheros-mark.svg ${icons}/scalable/apps/org.fedoraproject.AnacondaInstaller.svg
install -Dpm 0644 zypheros-mark.svg ${icons}/48x48/apps/org.fedoraproject.AnacondaInstaller.svg
install -Dpm 0644 zypheros-mark-small.svg ${icons}/symbolic/apps/org.fedoraproject.AnacondaInstaller-symbolic.svg

pix=%{buildroot}%{_datadir}/pixmaps
# Boot splash watermark source, the About page, and Cockpit (installer) branding
install -Dpm 0644 out/mark-252.png ${pix}/system-logo-white.png
install -Dpm 0644 out/mark-252.png ${pix}/fedora-logo-sprite.png
install -Dpm 0644 zypheros-mark.svg ${pix}/fedora-logo-sprite.svg
install -Dpm 0644 out/lockup-light-164.png ${pix}/fedora-logo.png
install -Dpm 0644 out/lockup-light-47.png ${pix}/fedora-logo-small.png
install -Dpm 0644 out/lockup-light-80.png ${pix}/fedora_logo_med.png
install -Dpm 0644 out/lockup-dark-80.png ${pix}/fedora_whitelogo_med.png
install -Dpm 0644 zypheros-kinetic-lockup-dark.svg ${pix}/fedora_whitelogo.svg
install -Dpm 0644 out/lockup-dark-43.png ${pix}/fedora-gdm-logo.png
install -Dpm 0644 out/logo-128.png ${pix}/bootloader/bootlogo_128.png
install -Dpm 0644 out/logo-256.png ${pix}/bootloader/bootlogo_256.png
install -Dpm 0644 out/favicon.png %{buildroot}%{_sysconfdir}/favicon.png

install -Dpm 0644 out/lockup-dark-64.png %{buildroot}%{_datadir}/plymouth/themes/spinner/watermark.png

ana=%{buildroot}%{_datadir}/anaconda/pixmaps
install -Dpm 0644 out/lockup-dark-69.png ${ana}/sidebar-logo.png
install -Dpm 0644 out/lockup-dark-36.png ${ana}/anaconda_header.png
install -Dpm 0644 out/sidebar-bg.png ${ana}/sidebar-bg.png
install -Dpm 0644 out/topbar-bg.png ${ana}/topbar-bg.png

install -d %{buildroot}%{_datadir}/zypheros-logos
install -pm 0644 zypheros-mark.svg zypheros-mark-small.svg zypheros-kinetic-lockup-dark.svg zypheros-kinetic-lockup-light.svg %{buildroot}%{_datadir}/zypheros-logos/


%files
%license COPYING
%{_datadir}/zypheros-logos/
%{_datadir}/icons/hicolor/*/apps/zypheros-logo-icon.*
%{_datadir}/icons/hicolor/*/apps/fedora-logo-icon.*
%{_datadir}/icons/hicolor/*/apps/start-here.svg
%{_datadir}/icons/hicolor/*/places/start-here.*
%{_datadir}/icons/hicolor/*/apps/org.fedoraproject.AnacondaInstaller*.svg
%{_datadir}/pixmaps/system-logo-white.png
%{_datadir}/pixmaps/fedora-logo-sprite.png
%{_datadir}/pixmaps/fedora-logo-sprite.svg
%{_datadir}/pixmaps/fedora-logo.png
%{_datadir}/pixmaps/fedora-logo-small.png
%{_datadir}/pixmaps/fedora_logo_med.png
%{_datadir}/pixmaps/fedora_whitelogo_med.png
%{_datadir}/pixmaps/fedora_whitelogo.svg
%{_datadir}/pixmaps/fedora-gdm-logo.png
%{_datadir}/pixmaps/bootloader/
%{_sysconfdir}/favicon.png
%{_datadir}/plymouth/themes/spinner/watermark.png
%{_datadir}/anaconda/pixmaps/sidebar-logo.png
%{_datadir}/anaconda/pixmaps/anaconda_header.png
%{_datadir}/anaconda/pixmaps/sidebar-bg.png
%{_datadir}/anaconda/pixmaps/topbar-bg.png


%changelog
* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial ZypherOS logos: circuit-Z mark and ZypherOS Kinetic wordmark
