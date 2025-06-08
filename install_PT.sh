#!/bin/bash
echo "Instalador do GrayWolfSystem"
echo "Os seguintes programas serão instalados durante este processo:"
echo "→ Python, Git, Pipx, Flask"
echo

echo "Qual distribuição Linux você está usando?"
echo "[1] ARCH   - (PACMAN)"
echo "[2] DEBIAN - (APT)"
echo "[3] TERMUX - (PKG)"
read -p ">> " distro

echo
echo "O que você deseja fazer?"
echo "[1] INSTALAR"
echo "[2] ATUALIZAR"
echo "[3] REMOVER"
read -p ">> " install

echo
echo "Onde o GWS deve ser instalado?"
echo "[1] PADRÃO (/opt/gws)"
echo "[2] CAMINHO PERSONALIZADO"
read -p ">> " path

if [ "$path" = "1" ]; then
    GWS_PATH="/opt/gws"
else
    read -p "Digite o caminho completo onde deseja instalar o GWS: " GWS_PATH
fi

instalar_pacotes() {
    echo "🔧 Instalando pacotes..."
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
            echo "❌ Opção de distribuição inválida!"
            exit 1
            ;;
    esac

    echo "📦 Instalando Flask com pipx..."
    pipx install flask
}

instalar_gws() {
    echo "⬇️ Clonando GrayWolfSystem em $GWS_PATH..."
    sudo mkdir -p "$GWS_PATH"
    sudo git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    sudo chown -R "$USER":"$USER" "$GWS_PATH"

    echo "Criando atalho para inicialização rápida..."
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" | sudo tee /usr/local/bin/gws-start > /dev/null
    sudo chmod +x /usr/local/bin/gws-start
    echo "✅ Atalho criado: execute 'gws-start' para iniciar o sistema!"

    echo
    echo "👤 Agora vamos criar o PRIMEIRO usuário (ADMIN) do GWS"
    read -p "→ Nome de usuário: " initial_user
    read -sp "→ Senha: " initial_password
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


    echo "✅ Usuário ADMIN inicial criado em: GWData/GWS_Users/users.json"
}

if [ "$install" = "1" ]; then
    instalar_pacotes
    instalar_gws
elif [ "$install" = "2" ]; then
    echo "⚙️ Atualizando repositório..."

    TEMP_DIR=$(mktemp -d)
    echo "→ Preservando GWLogs, GWData e GWFiles..."
    mv "$GWS_PATH/GWLogs" "$TEMP_DIR/GWLogs" 2>/dev/null
    mv "$GWS_PATH/GWData" "$TEMP_DIR/GWData" 2>/dev/null
    mv "$GWS_PATH/GWFiles" "$TEMP_DIR/GWFiles" 2>/dev/null

    sudo rm -rf "$GWS_PATH"
    sudo mkdir -p "$GWS_PATH"
    sudo chown -R "$USER":"$USER" "$GWS_PATH"
    
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "→ Restaurando GWLogs, GWData e GWFiles..."
    mv "$TEMP_DIR/GWLogs" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWData" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWFiles" "$GWS_PATH/" 2>/dev/null

    rm -rf "$TEMP_DIR"
    
    echo "✅ Atualização concluída!"

elif [ "$install" = "3" ]; then
    echo "🗑️ Removendo GWS..."
    sudo rm -rf "$GWS_PATH"
    sudo rm -f /usr/local/bin/gws-start
    echo "✅ GWS removido com sucesso!"
else
    echo "❌ Opção inválida."
    exit 1
fi

echo
echo "🚀 Processo concluído!"
