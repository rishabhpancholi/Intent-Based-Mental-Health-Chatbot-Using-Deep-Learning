function sendMessage() {
    // Get the user input from the input box and remove any leading/trailing spaces
    let userInput = document.getElementById('user-input').value.trim();

    // If input is empty, do nothing
    if (userInput == '') return;

    // Reference to the chat container where messages appear
    let chatContainer = document.getElementById("chat-container");

    // Create the user's message bubble aligned to the right
    let userMessage = `
        <div class="d-flex justify-content-end my-2">
            <div class="bot-message p-2">${userInput}</div>
        </div>`;

    // Append user's message to chat container
    chatContainer.insertAdjacentHTML("beforeend", userMessage);

    // Clear the input box
    document.getElementById("user-input").value = "";

    // Scroll to bottom after a short delay so the new message is visible
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);

    // Send user's input to backend using POST request
    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),  // Convert message to JSON
        headers: { "Content-Type": "application/json" } // Set header for JSON request
    })
    .then(response => response.json()) // Convert response to JSON
    .then(data => {
        // Create the bot's response bubble
        let botMessage = `<div class="bot-message p-2">${data.response}</div>`;

        // Append bot's message to chat container
        chatContainer.insertAdjacentHTML("beforeend", botMessage);

        // Scroll to bottom again to keep conversation in view
        setTimeout(() => {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 100);
    })
    .catch(error => console.error("Error:", error)); // Log any errors
}
