# ZypherOS Kinetic default wallpaper, as a KDE Plasma wallpaper package.
# Smaller sizes are generated at build time so Plasma can load the one
# closest to the screen resolution.

%global wallpaper_id ZypherOS-Kinetic

Name:           kinetic-backgrounds
Version:        0.2.0
Release:        1%{?dist}
Summary:        ZypherOS Kinetic desktop wallpaper
License:        LicenseRef-ZypherOS-Branding
URL:            https://github.com/zypher-systems/kinetic
BuildArch:      noarch

Source0:        zypheros-kinetic.jpg
Source1:        COPYING

BuildRequires:  ImageMagick

# Plasma's "Default" wallpaper, which Plasma Setup and new desktops fall back
# to, comes from whichever package provides system-backgrounds-kde. This one
# replaces Fedora's desktop-backgrounds-kde, as zypheros-logos replaces
# fedora-logos.
Provides:       system-backgrounds-kde = %{version}-%{release}
Obsoletes:      desktop-backgrounds-kde < 45
Conflicts:      desktop-backgrounds-kde

%description
The ZypherOS Kinetic wallpaper, packaged for KDE Plasma's wallpaper picker,
lock screen, and login screen, and set as Plasma's default wallpaper.


%prep
cp -p %{SOURCE0} %{SOURCE1} .


%build
mkdir -p images
# Plasma picks the image whose WIDTHxHEIGHT name best fits the screen
for width in 5504 3840 2560 1920; do
	magick zypheros-kinetic.jpg -resize ${width}x -strip -quality 90 images/tmp.jpg
	dims=$(magick identify -format '%%wx%%h' images/tmp.jpg)
	mv images/tmp.jpg images/${dims}.jpg
done
magick zypheros-kinetic.jpg -resize 400x250^ -gravity center -extent 400x250 -strip -quality 85 screenshot.jpg

cat > metadata.json << EOF
{
    "KPlugin": {
        "Authors": [ { "Name": "Zypher Systems" } ],
        "Id": "%{wallpaper_id}",
        "License": "LicenseRef-ZypherOS-Branding",
        "Name": "ZypherOS Kinetic"
    }
}
EOF


%install
dest=%{buildroot}%{_datadir}/wallpapers/%{wallpaper_id}
install -Dpm 0644 metadata.json ${dest}/metadata.json
install -Dpm 0644 screenshot.jpg ${dest}/contents/screenshot.jpg
install -d ${dest}/contents/images
install -pm 0644 images/*.jpg ${dest}/contents/images/
ln -s %{wallpaper_id} %{buildroot}%{_datadir}/wallpapers/Default


%files
%license COPYING
%{_datadir}/wallpapers/%{wallpaper_id}/
%{_datadir}/wallpapers/Default


%changelog
* Sun Sep 27 2026 Zypher Systems <zypher@zyphersystems.com> - 0.2.0-1
- Make the Kinetic wallpaper Plasma's default, replacing desktop-backgrounds-kde

* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial ZypherOS Kinetic wallpaper
