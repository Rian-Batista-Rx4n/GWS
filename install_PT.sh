#!/bin/bash
echo "Instalador do GrayWolfSystem"
echo "Os seguintes programas serão instalados durante este processo:"
echo "→ Python, Git, Flask, psutil, werkzeug"
echo

echo "Qual distribuição Linux você está utilizando?"
echo "[1] ARCH   - (PACMAN)"
echo "[2] DEBIAN - (APT)"
echo "[3] TERMUX - (PKG)"
read -p ">> " distro

echo
echo "O que você deseja fazer?"
echo "[1] INSTALAR"
echo "[2] ATUALIZAR"
echo "[3] REMOVER"
read -p ">> " acao

echo
echo "Onde o GWS deve ser instalado?"
echo "[1] PADRÃO (/opt/gws)"
echo "[2] CAMINHO PERSONALIZADO"
read -p ">> " caminho_opcao

# Definir caminho de instalação
if [ "$distro" = "3" ]; then
    GWS_PATH="$HOME/gws"
    BIN_PATH="$HOME/bin"
    mkdir -p "$BIN_PATH"
    export PATH="$BIN_PATH:$PATH"
else
    if [ "$caminho_opcao" = "1" ]; then
        GWS_PATH="/opt/gws"
    else
        read -p "Informe o caminho completo onde deseja instalar o GWS: " GWS_PATH
    fi
    BIN_PATH="/usr/local/bin"
fi

instalar_pacotes() {
    echo "🔧 Instalando pacotes necessários..."
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
            echo "❌ Opção de distribuição inválida!"
            exit 1
            ;;
    esac

    echo "📦 Instalando Flask, psutil e werkzeug..."

    if [ "$distro" = "3" ]; then
        pip install flask psutil werkzeug
    else
        pipx install flask
        pipx inject flask psutil werkzeug
    fi
}

instalar_gws() {
    echo "⬇️ Clonando o GrayWolfSystem em $GWS_PATH..."
    mkdir -p "$GWS_PATH"
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "🧩 Criando atalho: gws-start"
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" > "$BIN_PATH/gws-start"
    chmod +x "$BIN_PATH/gws-start"
    echo "✅ Atalho criado → Use o comando 'gws-start' para iniciar o GWS"

    echo
    echo "👤 Agora vamos criar o PRIMEIRO usuário (ADMIN) do GWS"
    read -p "→ Nome de usuário: " usuario_inicial
    read -sp "→ Senha: " senha_inicial
    echo

    mkdir -p "$GWS_PATH/GWData/GWUsers"

    criado_em=$(date +"%Y-%m-%d %H:%M:%S")

    cat <<EOF > "$GWS_PATH/GWData/GWUsers/users.json"
{
    "$usuario_inicial": {
        "senha": "$senha_inicial",
        "nivel": "admin",
        "criado_em": "$criado_em",
        "armazenamento_usado": 0
    }
}
EOF

    echo "✅ Usuário admin inicial criado em: GWData/GWUsers/users.json"

    echo
    echo "🚀 Testando execução do GWS..."
    cd "$GWS_PATH"
    python3 main.py &
    sleep 2
    kill $!
    echo "✅ Execução concluída com sucesso (teste passou)"
}

if [ "$acao" = "1" ]; then
    instalar_pacotes
    instalar_gws

elif [ "$acao" = "2" ]; then
    echo "⚙️ Atualizando repositório..."

    TEMP_DIR=$(mktemp -d)
    echo "→ Salvando GWLogs, GWData e GWFiles temporariamente..."
    mv "$GWS_PATH/GWLogs" "$TEMP_DIR/GWLogs" 2>/dev/null
    mv "$GWS_PATH/GWData" "$TEMP_DIR/GWData" 2>/dev/null
    mv "$GWS_PATH/GWFiles" "$TEMP_DIR/GWFiles" 2>/dev/null

    rm -rf "$GWS_PATH"
    mkdir -p "$GWS_PATH"
    
    git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    echo "→ Restaurando arquivos..."
    mv "$TEMP_DIR/GWLogs" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWData" "$GWS_PATH/" 2>/dev/null
    mv "$TEMP_DIR/GWFiles" "$GWS_PATH/" 2>/dev/null

    rm -rf "$TEMP_DIR"
    
    echo "✅ Atualização concluída!"

elif [ "$acao" = "3" ]; then
    echo "🗑️ Removendo o GWS..."
    rm -rf "$GWS_PATH"
    rm -f "$BIN_PATH/gws-start"
    echo "✅ GWS removido com sucesso!"
else
    echo "❌ Opção inválida."
    exit 1
fi

echo
echo "🎉 Instalação finalizada!"
