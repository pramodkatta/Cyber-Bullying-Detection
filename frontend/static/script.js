// Event listener to handle input type selection and display the appropriate input section
document.getElementById("inputType").addEventListener("change", function () {
    // Hide all input sections
    document.querySelectorAll(".inputSection").forEach(div => div.style.display = "none");

    // Show the selected input section
    document.getElementById(this.value + "Input").style.display = "block";
});

// Function to detect cyberbullying
async function detectCyberbullying() {
    const inputType = document.getElementById("inputType").value; // Get the selected input type
    let response;

    try {
        if (inputType === "text") {
            // Handle text input
            const text = document.getElementById("textMessage").value;

            // Validate that the text is not empty
            if (!text.trim()) {
                displayResult("Please enter some text.", "error");
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
                displayResult("Please upload a file.", "error");
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
        displayResult(`Result: ${result.prediction}`, "success");
    } catch (error) {
        // Handle errors gracefully
        console.error("Error:", error);
        displayResult(`Error: ${error.message}`, "error");
    }
}

// Function to display results
function displayResult(message, type) {
    const resultBox = document.getElementById("result-box");
    const result = document.getElementById("result");

    // Update the result text
    result.innerText = message;

    // Apply styling based on result type (success or error)
    if (type === "success") {
        resultBox.style.color = "green";
    } else if (type === "error") {
        resultBox.style.color = "red";
    }

    // Show the result box
    resultBox.classList.add("show");
}
