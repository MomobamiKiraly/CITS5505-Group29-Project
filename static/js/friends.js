document.addEventListener("DOMContentLoaded", function () {
  const chatInput = document.getElementById("chatInput");
  const chatBody = document.querySelector(".chat-body");
  const sendBtn = document.getElementById("sendBtn");
  const chatUserEl = document.getElementById("chatUser");

  function sendMessage() {
    const message = chatInput.value.trim();
    const receiver = chatUserEl.textContent;

    if (message && receiver) {
      fetch("/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ receiver, message })
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            const msg = document.createElement("p");
            msg.textContent = "You: " + message;
            chatBody.appendChild(msg);
            chatInput.value = "";
            scrollToBottom(chatBody);
          } else {
            alert("Message failed: " + data.message);
          }
        })
        .catch(error => {
          console.error("Send message error:", error);
          alert("Failed to send message.");
        });
    }
  }

  if (chatInput) {
    chatInput.addEventListener("keydown", e => {
      if (e.key === "Enter") sendMessage();
    });
  }

  if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
  }
});

function openChatModal(username) {
  const chatUserEl = document.getElementById("chatUser");
  const chatModalEl = document.getElementById("chatModal");
  const chatBody = document.querySelector(".chat-body");
  const chatInput = document.getElementById("chatInput");

  if (!username) return;

  chatUserEl.textContent = username;
  chatModalEl.style.display = "flex";
  chatBody.innerHTML = "<p><em>Loading chat...</em></p>";

  // Remove unread red dot
  const dot = document.querySelector(`.friend-list [data-username="${username}"] .unread-dot`);
  if (dot) dot.remove();

  fetch(`/get_messages/${username}`)
    .then(res => res.json())
    .then(messages => {
      chatBody.innerHTML = "";
      for (let m of messages) {
        const msg = document.createElement("p");
        const senderLabel = (m.from === CURRENT_USER_USERNAME) ? "You: " : `${m.from}: `;
        msg.textContent = senderLabel + m.content;
        chatBody.appendChild(msg);
      }
      scrollToBottom(chatBody);
    })
    .catch(error => {
      console.error("Get messages error:", error);
      chatBody.innerHTML = "<p><em>Failed to load chat messages.</em></p>";
    });

  chatInput.value = "";
  chatInput.focus();
}

function closeChatModal() {
  document.getElementById("chatModal").style.display = "none";
}

function scrollToBottom(container) {
  container.scrollTop = container.scrollHeight;
}