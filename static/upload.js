const subCategories = {
    audio: ["audio_no_category", "music", "podcast"],
    document: ["document_no_category", "excel", "powerpoint", "word", "pdf"],
    image: ["image_no_category", "photo", "screenshots"],
    text: ["text_no_category", "list", "note", "script"],
    video: ["video_no_category", "serie", "movie"],
    geral: ["no_subcategory"]
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
        opt.text = "No Subcategory";
        subSelect.appendChild(opt);
    }
});

const form = document.querySelector("form");
form.addEventListener("submit", function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const chooseFile = document.getElementById("chooseFile").value;
    const subCategory = document.getElementById("subCategory").value;
    const progress = document.getElementById("uploadProgress");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        alert("Select a file...");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append("file", fileInput.files[i]);
    }
    formData.append("chooseFile", chooseFile);
    formData.append("subCategory", subCategory);
    const isPublic = document.querySelector('input[name="public"]').checked;
    if (isPublic) {
        formData.append("public", "yes");
    }


    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/graywolf-upload-file", true);

    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const percent = Math.round((event.loaded / event.total) * 100);
            progress.style.display = "block";
            progress.value = percent;
            status.textContent = `Uploading...: ${percent}%`;
        }
    };

    xhr.onload = function () {
        if (xhr.status === 200) {
            status.textContent = "Upload Complete!";
        } else {
            status.textContent = "Upload Failed!";
        }
    };

    xhr.onerror = function () {
        status.textContent = "ERROR CONNECTION!.";
    };

    xhr.send(formData);
});