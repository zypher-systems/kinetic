loadTemplate("org.kde.plasma.desktop.defaultPanel")

var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    desktopsArray[j].wallpaperPlugin = 'org.kde.image';
}

// ZypherOS Kinetic: pin the everyday apps to the task manager
var allPanels = panels();
for (var i = 0; i < allPanels.length; i++) {
    var tasks = allPanels[i].widgets("org.kde.plasma.icontasks");
    for (var t = 0; t < tasks.length; t++) {
        tasks[t].currentConfigGroup = ["General"];
        tasks[t].writeConfig("launchers", [
            "preferred://filemanager",
            "preferred://browser",
            "applications:com.mitchellh.ghostty.desktop",
            "applications:codium.desktop",
            "applications:org.kde.discover.desktop",
            "applications:systemsettings.desktop"
        ]);
    }
}
