const subCategories = {
    audio: ["audio_no_category", "music", "podcast"],
    documents: ["documents_no_category", "excel", "powerpoint", "word", "pdf"],
    image: ["image_no_category", "photo", "screenshots"],
    text: ["text_no_category", "list", "note", "script"],
    video: ["video_no_category", "serie", "movie"],
    geral: ["sem_subcategoria"]
};

document.getElementById("chooseFile").addEventListener("change", function () {
    const selected = this.value;
    const subSelect = document.getElementById("subCategory");
    subSelect.innerHTML = "";

    if (subCategories[selected]) {
        subCategories[selected].forEach(sub => {
            const opt = document.createElement("option");
            opt.value = sub;
            opt.text = sub.charAt(0).toUpperCase() + sub.slice(1);
            subSelect.appendChild(opt);
        });
    } else {
        const opt = document.createElement("option");
        opt.value = "";
        opt.text = "Nenhuma subcategoria";
        subSelect.appendChild(opt);
    }
});

// Interceptar envio do formulário e usar AJAX
const form = document.querySelector("form");
form.addEventListener("submit", function (e) {
    e.preventDefault(); // impede envio tradicional

    const fileInput = document.getElementById("file");
    const chooseFile = document.getElementById("chooseFile").value;
    const subCategory = document.getElementById("subCategory").value;
    const progress = document.getElementById("uploadProgress");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        alert("Selecione um arquivo.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("chooseFile", chooseFile);
    formData.append("subCategory", subCategory);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/graywolf-upload-file", true);

    // Evento de progresso
    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const percent = Math.round((event.loaded / event.total) * 100);
            progress.style.display = "block";
            progress.value = percent;
            status.textContent = `Enviando: ${percent}%`;
        }
    };

    // Evento de fim
    xhr.onload = function () {
        if (xhr.status === 200) {
            status.textContent = "Upload concluído com sucesso!";
        } else {
            status.textContent = "Erro no upload.";
        }
    };

    xhr.onerror = function () {
        status.textContent = "Erro de conexão ao enviar.";
    };

    xhr.send(formData);
});