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

const uploadForm = document.getElementById("uploadForm");
uploadForm.addEventListener("submit", function (e) {
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

    let startTime = null;

    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const now = Date.now();
            if (!startTime) startTime = now;

            const elapsed = (now - startTime) / 1000; // segundos
            const uploadedMB = event.loaded / (1024 * 1024);
            const totalMB = event.total / (1024 * 1024);
            const speed = uploadedMB / elapsed; // MB/s

            const percent = Math.round((event.loaded / event.total) * 100);
            const remainingTime = (event.total - event.loaded) / (speed * 1024 * 1024); // segundos
            const minutes = Math.floor(remainingTime / 60);
            const seconds = Math.floor(remainingTime % 60);

            progress.style.display = "block";
            progress.value = percent;

            status.textContent = `Uploading... ${percent}% — approx. ${minutes}m ${seconds}s left`;
        }
    };


    xhr.onload = function () {
        if (xhr.status === 200) {
            status.textContent = "✅ Upload Complete!";
            status.style.color = "lightgreen";
        } else {
            status.textContent = "❌ Upload Failed!";
            status.style.color = "red";
        }
    };


    xhr.onerror = function () {
        status.textContent = "❌ ERROR: Connection Failed!";
        status.style.color = "red";
    };


    xhr.send(formData);
});