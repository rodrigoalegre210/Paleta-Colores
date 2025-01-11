document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const paletteForm = document.getElementById("palette-form");
    const contrastForm = document.getElementById("contrast-form");

    const colorPreview = document.getElementById("color-preview");
    const palettePreview = document.getElementById("palette-preview");
    const contrastResult = document.getElementById("contrast-result");
    const imagePreviewContainer = document.getElementById("image-preview-conteiner");
    const imagePreview = document.getElementById("image-preview");
    const imageText = document.getElementById("image-text");

    // Función para configurar la copia de colores y mostrar tooltip
    function setupColorCopy() {
        const colorBlocks = document.querySelectorAll(".color-block");
        colorBlocks.forEach(block => {
            block.addEventListener("click", () => {
                const color = block.textContent;
                navigator.clipboard.writeText(color).then(() => {
                    showTooltip(block, `Copiado: ${color}`);
                });
            });
        });
    }

    // Función para mostrar el tooltip
    function showTooltip(element, message) {
        const tooltip = document.createElement("div");
        tooltip.classList.add("tooltip");
        tooltip.textContent = message;

        // Posicionar el tooltip sobre el elemento
        const rect = element.getBoundingClientRect();
        tooltip.style.top = `${rect.top - 10}px`;
        tooltip.style.left = `${rect.left + rect.width / 2}px`;

        // Agregar el tooltip al documento
        document.body.appendChild(tooltip);

        // Remover el tooltip después de 2 segundos
        setTimeout(() => tooltip.remove(), 2000);
    }

    // Función para manejar la vista previa de la imagen
    function handleImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            imagePreview.src = event.target.result;
            imagePreview.style.display = "block";
            imageText.style.display = "none";
        };
        reader.readAsDataURL(file);
    }

    // Evento de cambio en el input de archivo para actualizar la vista previa
    document.getElementById("file-input").addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            handleImagePreview(file);
        } else {
            imagePreview.style.display = "none";
            imageText.style.display = "block";
        }
    });

    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(uploadForm);

        const fileInput = document.getElementById("file-input");
        if (!fileInput.files.length) {
            alert("Por favor, selecciona un archivo.");
            return;
        }

        try {
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error || "Error al procesar la imagen.");
                return;
            }

            const data = await response.json();
            if (data.Colores) {
                colorPreview.innerHTML = data.Colores
                    .map(color => `<div class="color-block" style="background-color: ${color}">${color}</div>`)
                    .join("");
                setupColorCopy();
            } else {
                alert("No se encontraron colores en la imagen.");
            }
        } catch (error) {
            alert("Error de red: " + error.message);
        }
    });

    paletteForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const colorsInput = document.getElementById("colors-input").value;
        const colors = colorsInput.split(",").map(color => color.trim());

        try {
            const response = await fetch("/api/palette", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ colors }),
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error);
                return;
            }

            const data = await response.json();
            palettePreview.innerHTML = data.palette
                .map(color => `<div class="color-block" style="background-color: ${color}">${color}</div>`)
                .join("");
            setupColorCopy();
        } catch (error) {
            alert("Error generating palette. Please try again.");
        }
    });

    contrastForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const color1 = document.getElementById("color1-input").value.trim();
        const color2 = document.getElementById("color2-input").value.trim();

        try {
            const response = await fetch("/api/contrast", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ color1, color2 }),
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error);
                return;
            }

            const data = await response.json();
            contrastResult.textContent = `Relación de Contraste: ${data.radio_constraste}`;
        } catch (error) {
            alert("Error analyzing contrast. Please try again.");
        }
    });
});
