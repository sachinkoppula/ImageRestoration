document.getElementById("upload").addEventListener("change", function () {
    const file = this.files[0];
    const fileName = file?.name || "Choose an image";
    document.getElementById("file-name").textContent = fileName;

    if (file) {
        const inputImage = document.getElementById("input-image");
        const reader = new FileReader();

        reader.onload = function (e) {
            // Display the selected input image
            inputImage.src = e.target.result;
            inputImage.style.display = "block"; // Make sure the input image is visible
        };

        reader.readAsDataURL(file);
    }
});

document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent default form submission
    const formData = new FormData(this); // Gather form data

    const restoredImage = document.getElementById("restored-image");
    const restoringText = document.getElementById("restoring-text");

    restoringText.style.display = "block"; // Show restoring text
    restoredImage.style.display = "none"; // Hide the restored image initially

    try {
        const response = await fetch("/restore", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob(); // Get the restored image
            const url = URL.createObjectURL(blob); // Create a temporary URL

            restoredImage.src = url; // Set the restored image's source
            restoredImage.style.display = "block"; // Show the restored image
            restoringText.style.display = "none"; // Hide the restoring text
        } else {
            restoringText.textContent = "Failed to restore image. Try again.";
        }
    } catch (err) {
        console.error(err);
        restoringText.textContent = "An error occurred. Please try again.";
    }
});
