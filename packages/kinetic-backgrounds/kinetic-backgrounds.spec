# ZypherOS Kinetic default wallpaper, as a KDE Plasma wallpaper package.
# Smaller sizes are generated at build time so Plasma can load the one
# closest to the screen resolution.

%global wallpaper_id ZypherOS-Kinetic

Name:           kinetic-backgrounds
Version:        0.2.0
Release:        2%{?dist}
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
lock screen, and login screen, with a blurred version as Plasma's default
wallpaper, which Plasma Setup shows behind its welcome text.


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

# A blurred, darkened version, as Plasma's "Default" wallpaper. Plasma Setup
# (Fedora's build) draws its welcome text over Default's 5120x2880.jxl, or
# 1440x2960.jxl on portrait screens, from images/ or, with the dark theme,
# images_dark/; over the sharp wallpaper the text lands on the wordmark.
# Blurred at a quarter of the size, where it is fast; the portrait crop is
# centred on the Z mark.
mkdir -p blur
backdrop=(-blur 0x10 -fill '#0B1220' -colorize 40%% -strip -quality 90)
magick zypheros-kinetic.jpg -resize 1280x720^ -gravity center -extent 1280x720 "${backdrop[@]}" -resize 5120x2880 blur/5120x2880.jxl
magick zypheros-kinetic.jpg -resize x740 -crop 360x740+225+0 +repage "${backdrop[@]}" -resize 1440x2960 blur/1440x2960.jxl
magick blur/5120x2880.jxl -resize 400x250^ -gravity center -extent 400x250 -quality 85 blur/screenshot.jpg

cat > blur/metadata.json << EOF
{
    "KPlugin": {
        "Authors": [ { "Name": "Zypher Systems" } ],
        "Id": "%{wallpaper_id}-Blur",
        "License": "LicenseRef-ZypherOS-Branding",
        "Name": "ZypherOS Kinetic (blurred)"
    }
}
EOF


%install
dest=%{buildroot}%{_datadir}/wallpapers/%{wallpaper_id}
install -Dpm 0644 metadata.json ${dest}/metadata.json
install -Dpm 0644 screenshot.jpg ${dest}/contents/screenshot.jpg
install -d ${dest}/contents/images
install -pm 0644 images/*.jpg ${dest}/contents/images/

blur=%{buildroot}%{_datadir}/wallpapers/%{wallpaper_id}-Blur
install -Dpm 0644 blur/metadata.json ${blur}/metadata.json
install -Dpm 0644 blur/screenshot.jpg ${blur}/contents/screenshot.jpg
install -d ${blur}/contents/images ${blur}/contents/images_dark
for image in 5120x2880.jxl 1440x2960.jxl; do
	install -pm 0644 blur/${image} ${blur}/contents/images/
	# The same images for the dark theme
	ln -s ../images/${image} ${blur}/contents/images_dark/${image}
done
ln -s %{wallpaper_id}-Blur %{buildroot}%{_datadir}/wallpapers/Default


%files
%license COPYING
%{_datadir}/wallpapers/%{wallpaper_id}/
%{_datadir}/wallpapers/%{wallpaper_id}-Blur/
%{_datadir}/wallpapers/Default


%changelog
* Fri Oct 02 2026 Zypher Systems <zypher@zyphersystems.com> - 0.2.0-2
- Plasma's default wallpaper, which Plasma Setup draws its text over, is now
  a blurred, darkened version of the Kinetic wallpaper

* Sun Sep 27 2026 Zypher Systems <zypher@zyphersystems.com> - 0.2.0-1
- Make the Kinetic wallpaper Plasma's default, replacing desktop-backgrounds-kde
- Add the JPEG XL sizes Plasma Setup loads

* Sat Sep 26 2026 Zypher Systems <zypher@zyphersystems.com> - 0.1.0-1
- Initial ZypherOS Kinetic wallpaper
