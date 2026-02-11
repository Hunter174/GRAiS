let currentAudio = null;

function playAudioBase64(base64Wav) {
    // Stop previous audio to avoid overlap
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    const audio = new Audio(`data:audio/wav;base64,${base64Wav}`);
    currentAudio = audio;

    audio.play().catch(err => {
        console.error("Audio playback failed:", err);
    });
}


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

    // show typing indicator immediately
    showThinking();
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

    // remove typing indicator
    removeThinking();

    if (data.error) {
        appendMessage("bot", data.error);
        return;
    }

    appendMessage("bot", data.response);

    if (enable_tts && data.audio) {
        playAudioBase64(data.audio);
    }
}

async function resetChat() {
    await fetch("/chat/reset/", {method: "POST"});
    location.reload();
}

let thinkingNode = null;

function showThinking() {
    const log = document.getElementById("log");

    const msg = document.createElement("div");
    msg.className = "msg bot thinking";

    const bubble = document.createElement("div");
    bubble.className = "bubble"; // 👈 IMPORTANT

    bubble.innerHTML = `
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    `;

    msg.appendChild(bubble);
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;

    thinkingNode = msg;
}

function removeThinking() {
    if (thinkingNode) {
        thinkingNode.remove();
        thinkingNode = null;
    }
}
