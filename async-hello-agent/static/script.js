document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const clearBtn = document.getElementById("clear-btn");

    // Scroll to bottom helper
    const scrollToBottom = () => {
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Add message to chat UI
    const appendMessage = (content, sender) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        
        // Use marked.js for markdown rendering if it's an assistant message
        if (sender === "assistant") {
            contentDiv.innerHTML = marked.parse(content);
        } else {
            contentDiv.textContent = content;
        }
        
        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();
    };

    // Show loading indicator
    const showLoading = () => {
        const loadingDiv = document.createElement("div");
        loadingDiv.className = "loading";
        loadingDiv.id = "loading-indicator";
        loadingDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;
        chatBox.appendChild(loadingDiv);
        scrollToBottom();
    };

    // Remove loading indicator
    const hideLoading = () => {
        const loadingDiv = document.getElementById("loading-indicator");
        if (loadingDiv) {
            loadingDiv.remove();
        }
    };

    // Send message to API and handle streaming
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Clear input and show user message
        userInput.value = "";
        appendMessage(message, "user");
        
        showLoading();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            hideLoading();
            
            if (!response.ok) {
                appendMessage(`Error: ${response.statusText}`, "assistant");
                return;
            }

            // Create empty assistant message div
            const messageDiv = document.createElement("div");
            messageDiv.className = `message assistant-message`;
            const contentDiv = document.createElement("div");
            contentDiv.className = "message-content";
            messageDiv.appendChild(contentDiv);
            chatBox.appendChild(messageDiv);
            scrollToBottom();

            // Setup stream reader
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let fullText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                fullText += chunk;
                contentDiv.innerHTML = marked.parse(fullText);
                scrollToBottom();
            }

        } catch (error) {
            hideLoading();
            appendMessage(`Connection Error: Make sure the server is running.`, "assistant");
            console.error(error);
        }
    };

    // Event Listeners
    sendBtn.addEventListener("click", sendMessage);

    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    clearBtn.addEventListener("click", () => {
        chatBox.innerHTML = `
            <div class="message assistant-message">
                <div class="message-content">Chat cleared! How can I help you today?</div>
            </div>
        `;
    });
});
