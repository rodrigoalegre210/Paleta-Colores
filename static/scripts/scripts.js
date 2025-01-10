document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const paletteForm = document.getElementById("palette-form");
    const contrastForm = document.getElementById("contrast-form");

    const colorPreview = document.getElementById("color-preview");
    const palettePreview = document.getElementById("palette-preview");
    const contrastResult = document.getElementById("contrast-result");

    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(uploadForm);
        try {
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json();
                alert(error.error);
                return;
            }

            const data = await response.json();
            colorPreview.innerHTML = data.colors
                .map(color => `<div class="color-block" style="background-color: ${color}">${color}</div>`)
                .join("");
        } catch (error) {
            alert("Error uploading the image. Please try again.");
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
            contrastResult.textContent = `Contrast Ratio: ${data.contrast_ratio}`;
        } catch (error) {
            alert("Error analyzing contrast. Please try again.");
        }
    });
});