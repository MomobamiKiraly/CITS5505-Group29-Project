document.getElementById('chat-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const userInput = document.getElementById('user-input').value.trim();
  if (!userInput) return;

  const userMessage = document.createElement('div');
  userMessage.className = 'chatbot-message user';
  userMessage.textContent = "You: " + userInput;
  document.getElementById('messages').appendChild(userMessage);

  const botReply = document.createElement('div');
  botReply.className = 'chatbot-message bot';
  botReply.textContent = "Bot: (thinking...)";
  document.getElementById('messages').appendChild(botReply);

  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: userInput })
  })
  .then(response => response.json())
  .then(data => {
    if (data.reply) {
      botReply.textContent = "Bot: " + data.reply;
    } else if (data.error) {
      botReply.textContent = "Bot error: " + data.error;
    } else {
      botReply.textContent = "Bot: Unexpected response.";
    }
  })
  .catch(error => {
    botReply.textContent = "Bot: Failed to connect to server.";
    console.error(error);
  });

  document.getElementById('user-input').value = '';
  document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
});