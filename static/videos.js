document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".load-video-btn");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const src = button.getAttribute("data-src");
            const container = button.nextElementSibling;

            // Evita carregar duas vezes
            if (container.innerHTML.trim() !== "") return;

            container.innerHTML = `
                <video width="320" height="180" controls autoplay>
                    <source src="${src}" type="video/mp4">
                    Your browser does not support the video.
                </video>
            `;

            button.remove(); // Remove o botão após clicar (opcional)
        });
    });

    // Correção: adicionar handler para os forms de delete
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const filePath = form.getAttribute("data-file-path");
            const hiddenInput = form.querySelector("input[name='file_path']");
            hiddenInput.value = filePath;
            // opcional: console.log("Deletando:", filePath);
        });
    });
});
