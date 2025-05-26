function abrirModal(src) {
    document.getElementById("imagem-ampliada").src = src;
    document.getElementById("modal").style.display = "block";
}

function fecharModal() {
    document.getElementById("modal").style.display = "none";
}