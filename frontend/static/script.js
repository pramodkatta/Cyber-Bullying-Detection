// Handle input type selection and display corresponding input section
document.getElementById("inputType").addEventListener("change", function () {
    // Hide all input sections
    document.querySelectorAll(".inputSection").forEach(div => div.style.display = "none");

    // Show the selected input section
    document.getElementById(this.value + "Input").style.display = "block";
});

// Function to detect cyberbullying based on input type
async function detectCyberbullying() {
    const inputType = document.getElementById("inputType").value; // Get the selected input type
    let response;

    try {
        if (inputType === "text") {
            // Handle text input
            const text = document.getElementById("textMessage").value;

            // Validate that the text is not empty
            if (!text.trim()) {
                document.getElementById("result").innerText = "Please enter some text.";
                return;
            }

            // Send the POST request to the backend for text input
            response = await fetch("http://127.0.0.1:8000/predict/text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text.trim() }) // Trim any extra whitespace
            });
        } else {
            // Handle file inputs (image or audio)
            const fileInput = document.getElementById(inputType + "File");

            // Validate that a file is selected
            if (fileInput.files.length === 0) {
                document.getElementById("result").innerText = "Please upload a file.";
                return;
            }

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            // Send the POST request to the backend for image or audio input
            response = await fetch(`http://127.0.0.1:8000/predict/${inputType}`, {
                method: "POST",
                body: formData
            });
        }

        // Check if the response is OK
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        // Parse the JSON response
        const result = await response.json();

        // Display the prediction result
        document.getElementById("result").innerText = `Result: ${result.prediction}`;
    } catch (error) {
        // Handle errors gracefully
        console.error("Error:", error);
        document.getElementById("result").innerText = `Error: ${error.message}`;
    }
}
