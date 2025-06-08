#!/bin/bash
echo "GrayWolfSystem Installer"
echo "The following programs will be installed during this process:"
echo "→ Python, Git, Pipx, Flask"
echo

echo "Which Linux distribution are you using?"
echo "[1] ARCH   - (PACMAN)"
echo "[2] DEBIAN - (APT)"
echo "[3] TERMUX - (PKG)"
read -p ">> " distro

echo
echo "What do you want to do?"
echo "[1] INSTALL"
echo "[2] UPDATE"
echo "[3] REMOVE"
read -p ">> " install

echo
echo "Where is / should GWS be installed?"
echo "[1] DEFAULT (/opt/gws)"
echo "[2] CUSTOM PATH"
read -p ">> " path

if [ "$path" = "1" ]; then
    GWS_PATH="/opt/gws"
else
    read -p "Enter the full path where you want to install GWS: " GWS_PATH
fi

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

    echo "📦 Installing Flask with pipx..."
    pipx install flask
}

install_gws() {
    echo "⬇️ Cloning GrayWolfSystem to $GWS_PATH..."
    sudo mkdir -p "$GWS_PATH"
    sudo git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    sudo chown -R "$USER":"$USER" "$GWS_PATH"

    echo "Creating shortcut for quick launch..."
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" | sudo tee /usr/local/bin/gws-start > /dev/null
    sudo chmod +x /usr/local/bin/gws-start
    echo "✅ Shortcut created: run 'gws-start' to launch the system!"

    echo
    echo "👤 Now let's create the FIRST user (ADMIN) for GWS"
    read -p "→ Username: " initial_user
    read -sp "→ Password: " initial_password
    echo

    mkdir -p "$GWS_PATH/GWData/GWS_Users"

    created_at=$(date +"%Y-%m-%d %H:%M:%S")

    cat <<EOF > "$GWS_PATH/GWData/GWUsers/users.json"
{
    "$initial_user": {
        "senha": "$initial_password",
        "nivel": "admin",
        "criado_em": "$created_at",
        "armazenamento_usado": 0
    }
}
EOF


    echo "✅ Initial admin user created in: GWData/GWS_Users/users.json"
}

if [ "$install" = "1" ]; then
    install_packages
    install_gws
elif [ "$install" = "2" ]; then
    echo "⚙️ Updating repository..."

    TEMP_DIR=$(mktemp -d)
    echo "→ Preserving GWLogs, GWData and GWFiles..."
    mv "$GWS_PATH/GWLogs" "$TEMP_DIR/GWLogs" 2>/dev/null
    mv "$GWS_PATH/GWData" "$TEMP_DIR/GWData" 2>/dev/null
    mv "$GWS_PATH/GWFiles" "$TEMP_DIR/GWFiles" 2>/dev/null

    sudo rm -rf "$GWS_PATH"
    sudo mkdir -p "$GWS_PATH"
    sudo chown -R "$USER":"$USER" "$GWS_PATH"
    
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "→ Restoring GWLogs and GWData..."
    mv "$TEMP_DIR/GWLogs" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWData" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWFiles" "$GWS_PATH/" 2>/dev/null

    rm -rf "$TEMP_DIR"
    
    echo "✅ Update completed!"

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
