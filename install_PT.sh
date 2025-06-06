#!/bin/bash

echo "GrayWolfSystem Installer"
echo "Vamos instalar os seguintes programas até o final do instalador:"
echo "→ Python, Git, Pipx, Flask"
echo

# Menu de seleção da distribuição
echo "Qual distro você usa?"
echo "[1] ARCH   - (PACMAN)"
echo "[2] DEBIAN - (APT)"
echo "[3] TERMUX - (PKG)"
read -p ">> " distro

# Ação desejada
echo
echo "Você deseja:"
echo "[1] INSTALAR"
echo "[2] ATUALIZAR"
echo "[3] REMOVER"
read -p ">> " install

# Caminho de instalação
echo
echo "Onde está/fica a pasta GWS?"
echo "[1] PADRÃO (/opt/gws)"
echo "[2] CUSTOMIZADA"
read -p ">> " path

# Definindo caminho
if [ "$path" = "1" ]; then
    GWS_PATH="/opt/gws"
else
    read -p "Digite o caminho completo onde deseja instalar o GWS: " GWS_PATH
fi

# Função para instalar pacotes
install_packages() {
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
            echo "❌ Opção de distro inválida!"
            exit 1
            ;;
    esac

    # Instala Flask via pipx
    echo "📦 Instalando Flask com pipx..."
    pipx install flask
}

# Função para instalar o GWS
install_gws() {
    echo "⬇️ Clonando o GrayWolfSystem para $GWS_PATH..."
    sudo mkdir -p "$GWS_PATH"
    sudo git clone https://github.com/Rian-Batista-Rx4n/GWS "$GWS_PATH"

    sudo chown -R "$USER":"$USER" "$GWS_PATH"

    echo "Criando atalho para execução rápida..."
    echo -e "#!/bin/bash\ncd $GWS_PATH\npython3 main.py" | sudo tee /usr/local/bin/gws-start > /dev/null
    sudo chmod +x /usr/local/bin/gws-start
    echo "✅ Atalho criado: use o comando 'gws-start' para iniciar o sistema!"
}

# Execução conforme ação escolhida
if [ "$install" = "1" ]; then
    install_packages
    install_gws
elif [ "$install" = "2" ]; then
    echo "⚙️ Atualizando repositório..."
    cd "$GWS_PATH" && git pull
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
echo "🚀 Instalação finalizada!"
