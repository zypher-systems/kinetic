function update --description 'Update system packages and Flatpaks'
    echo "🔄 Updating system packages..."
    sudo dnf upgrade --refresh $argv
    and if command -q flatpak
        echo "🔄 Updating Flatpaks..."
        flatpak update
    end
end
