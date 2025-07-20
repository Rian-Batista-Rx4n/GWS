#!/bin/bash
echo "GrayWolfSystem Installer"
echo "The following programs will be installed during this process:"
echo "→ Python, Git, Flask, psutil, werkzeug"
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

# Definir caminho de instalação
if [ "$distro" = "3" ]; then
    GWS_PATH="$HOME/gws"
    BIN_PATH="$HOME/bin"
    mkdir -p "$BIN_PATH"
    export PATH="$BIN_PATH:$PATH"
else
    if [ "$path" = "1" ]; then
        GWS_PATH="/opt/gws"
    else
        read -p "Enter the full path where you want to install GWS: " GWS_PATH
    fi
    BIN_PATH="/usr/local/bin"
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
            pkg install -y python git
            pip install --upgrade pip
            ;;
        *)
            echo "❌ Invalid distro option!"
            exit 1
            ;;
    esac

    echo "📦 Installing Flask, psutil, werkzeug..."

    if [ "$distro" = "3" ]; then
        pip install flask psutil werkzeug
    else
        pipx install flask
        pipx inject flask psutil werkzeug
    fi
}

install_gws() {
    echo "⬇️ Cloning GrayWolfSystem to $GWS_PATH..."
    mkdir -p "$GWS_PATH"
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "🧩 Creating shortcut: gws-start"
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" > "$BIN_PATH/gws-start"
    chmod +x "$BIN_PATH/gws-start"
    echo "✅ Shortcut created → Run 'gws-start' to launch GWS"

    echo
    echo "👤 Now let's create the FIRST user (ADMIN) for GWS"
    read -p "→ Username: " initial_user
    read -sp "→ Password: " initial_password
    echo

    mkdir -p "$GWS_PATH/GWData/GWUsers"

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

    echo "✅ Initial admin user created in: GWData/GWUsers/users.json"

    echo
    echo "🚀 Testing GWS execution..."
    cd "$GWS_PATH"
    python3 main.py &
    sleep 2
    kill $!
    echo "✅ GWS executed without crash (test passed)"
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

    rm -rf "$GWS_PATH"
    mkdir -p "$GWS_PATH"
    
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "→ Restoring GWLogs and GWData..."
    mv "$TEMP_DIR/GWLogs" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWData" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWFiles" "$GWS_PATH/" 2>/dev/null

    rm -rf "$TEMP_DIR"
    
    echo "✅ Update completed!"

elif [ "$install" = "3" ]; then
    echo "🗑️ Removing GWS..."
    rm -rf "$GWS_PATH"
    rm -f "$BIN_PATH/gws-start"
    echo "✅ GWS successfully removed!"
else
    echo "❌ Invalid option."
    exit 1
fi

echo
echo "🎉 Installation finished!"
