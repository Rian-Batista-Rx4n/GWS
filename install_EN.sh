#!/bin/bash

echo "GrayWolfSystem Installer"
echo "The following programs will be installed during this process:"
echo "→ Python, Git, Pipx, Flask"
echo

# Distro selection menu
echo "Which Linux distribution are you using?"
echo "[1] ARCH   - (PACMAN)"
echo "[2] DEBIAN - (APT)"
echo "[3] TERMUX - (PKG)"
read -p ">> " distro

# Desired action
echo
echo "What do you want to do?"
echo "[1] INSTALL"
echo "[2] UPDATE"
echo "[3] REMOVE"
read -p ">> " install

# Installation path
echo
echo "Where is / should GWS be installed?"
echo "[1] DEFAULT (/opt/gws)"
echo "[2] CUSTOM PATH"
read -p ">> " path

# Define path
if [ "$path" = "1" ]; then
    GWS_PATH="/opt/gws"
else
    read -p "Enter the full path where you want to install GWS: " GWS_PATH
fi

# Package installation function
install_packages() {
    echo "🔧 Installing packages..."
    case "$distro" in
        1)
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm python git pipx
            ;;
        2)
            sudo apt update && sudo apt upgrade -y
            sudo apt install -y python3 python3-pip pipx git
            ;;
        3)
            pkg update -y && pkg upgrade -y
            pkg install -y python git pipx
            ;;
        *)
            echo "❌ Invalid distro option!"
            exit 1
            ;;
    esac

    # Install Flask using pipx
    echo "📦 Installing Flask with pipx..."
    pipx install flask
}

# GWS installation function
install_gws() {
    echo "⬇️ Cloning GrayWolfSystem to $GWS_PATH..."
    sudo mkdir -p "$GWS_PATH"
    sudo git clone https://github.com/Rian-Batista-Rx4n/web-files-manager-graywolfsystem "$GWS_PATH"

    sudo chown -R "$USER":"$USER" "$GWS_PATH"

    echo "Creating shortcut for quick launch..."
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" | sudo tee /usr/local/bin/gws-start > /dev/null
    sudo chmod +x /usr/local/bin/gws-start
    echo "✅ Shortcut created: run 'gws-start' to launch the system!"
}

# Run based on user choice
if [ "$install" = "1" ]; then
    install_packages
    install_gws
elif [ "$install" = "2" ]; then
    echo "⚙️ Updating repository..."
    cd "$GWS_PATH" && git pull
elif [ "$install" = "3" ]; then
    echo "🗑️ Removing GWS..."
    sudo rm -rf "$GWS_PATH"
    sudo rm -f /usr/local/bin/gws-start
    echo "✅ GWS successfully removed!"
else
    echo "❌ Invalid option."
    exit 1
fi

echo
echo "🚀 Installation completed!"
