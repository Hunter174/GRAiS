function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        send();
    }
}

function appendMessage(role, text) {
    const log = document.getElementById("log");

    const msg = document.createElement("div");
    msg.className = `msg ${role}`;

    const bubble = document.createElement("div");

    if (role === "bot") {
        bubble.innerHTML = marked.parse(text);
    } else {
        bubble.textContent = text;
    }

    msg.appendChild(bubble);
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;
}


async function send() {
    const input = document.getElementById("input");
    const text = input.value.trim();
    if (!text) return;

    const persona = document.getElementById("persona").value;
    const tools = document.getElementById("tools").value;
    const enable_tts = document.getElementById("enable_tts").checked;

    appendMessage("user", text);
    input.value = "";

    const res = await fetch("/chat/api/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: text,
            persona,
            tools,
            enable_tts,
        }),
    });

    const data = await res.json();

    if (data.error) {
        appendMessage("bot", data.error);
    } else {
        appendMessage("bot", data.response);
    }
}

async function resetChat() {
    await fetch("/chat/reset/", {method: "POST"});
    location.reload();
}