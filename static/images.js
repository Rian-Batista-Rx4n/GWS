function abrirModal(src) {
    document.getElementById("imagem-ampliada").src = src;
    document.getElementById("modal").style.display = "block";
}

function fecharModal() {
    document.getElementById("modal").style.display = "none";
}

function mostrarLixeira(el) {
    const botao = el.querySelector('.botao-delete');
    if (botao) botao.style.display = 'block';
}

function ocultarLixeira(el) {
    const botao = el.querySelector('.botao-delete');
    if (botao) botao.style.display = 'none';
}

function abrirModal(src) {
    var modal = document.getElementById("modal");
    var imagemAmpliada = document.getElementById("imagem-ampliada");
    var filePathInput = document.getElementById("file_path_input");

    modal.style.display = "block";
    imagemAmpliada.src = src;

    var pathRelativo = src.split("/imagem/")[1];

    if (!pathRelativo || pathRelativo.endsWith("/") || !pathRelativo.match(/\.\w+$/)) {
        console.warn("Path da imagem inválido ou é um diretório:", pathRelativo);
        filePathInput.value = "";
        return;
    }

    var filePath = "GWFiles/image/" + pathRelativo;

    filePathInput.value = filePath;

    console.log("Arquivo para deletar:", filePath);  // debug no console
}


function fecharModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}

