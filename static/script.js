function sendMessage(){
    let userInput = document.getElementById('user-input').value.trim();
    if(userInput=='') return;

    let chatContainer = document.getElementById("chat-container");

    let userMessage = `<div class="d-flex justify-content-end my-2">
                      <div class="bot-message p-2">${userInput}</div>
                   </div>`;

    // chatContainer.innerHTML += userMessage;
    chatContainer.insertAdjacentHTML("beforeend", userMessage);
    document.getElementById("user-input").value = "";

    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);

    fetch("/chat",{
        method: "POST",
        body:JSON.stringify({message : userInput}),
        headers: {"Content-Type": "application/json"}
    })
    .then(response => response.json())
    .then(data=>{
        let botMessage = `<div class="bot-message p-2">${data.response}</div>`;
        // chatContainer.innerHTML += botMessage;
        chatContainer.insertAdjacentHTML("beforeend", botMessage);

        setTimeout(() => {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 100);
    })
    .catch(error=>console.error("Error:", error));
}