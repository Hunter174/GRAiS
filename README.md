# GRAiS  
**G**enerally **R**eliable **A**rtificial **I**ntelligence **S**ystem

## Welcome!

GRAiS is a personal project inspired by JARVIS, designed to evolve into a reliable and intelligent virtual assistant. This system is being built with a focus on enhancing productivity, interaction, and automation, bringing a smarter way to manage daily tasks.

### Project Goals

- **Calendar Assistant**  
  Seamlessly manage your schedule by integrating with Google Calendar. GRAiS will provide proactive meeting reminders, schedule suggestions, and help avoid conflicts.
  
- **To-Do List Tracker**  
  Efficiently create, track, and complete tasks using an open-source to-do list integration. GRAiS will prioritize tasks and help you stay organized.
  
- **Text to Speech (TTS)**  
  Real-time communication through TTS with dynamic sine wave visualizations, bringing a futuristic, responsive element to the conversation.
  
- **Speech to Text (STT)**  
  Real-time speech recognition, paired with engaging sine wave visualizations, allowing natural conversations and command input.

---

# Getting Started

GRAiS is designed to run **fully locally** using **Ollama** for language models. This provides fast inference, zero API costs, and strong privacy guarantees.

---
## Ollama App Setup (Required – Tool Calling Enabled)

GRAiS **requires the Ollama desktop application** and **a model that supports tool calling**.  
Command-line–only or unsupported models will **not work**.

---

### Step 1: Install the Ollama Desktop App

Download and install the official Ollama application:

👉 https://ollama.com/download

The desktop app is **required**. It installs:
- A background inference service
- The Ollama model manager
- Tool-calling–capable runtime support

After installation, **launch the Ollama app**.

---

### Step 2: Open the Ollama Chat Interface

Once the app is running, you should see the Ollama chat window.

If you do not see the chat UI:
- Ensure the app is running (tray/menu bar)
- Restart Ollama if needed

---

### Step 3: Select the Required Model (Critical)

In the **model selector dropdown** at the bottom of the chat window, select:

```text
gpt-oss:20b-cloud
```

⚠️ **This step is mandatory.**

This model is required because it:

- Supports **tool calling**
- Correctly emits **structured tool invocation messages**
- Is compatible with **LangChain’s tool router**

Other models may appear to work but will **fail silently** when tools are invoked.

---

### Step 4: Verify the Model Is Active

Confirm that the chat UI shows:

```text
Model: gpt-oss:20b-cloud
```

Send a test message such as:

```text
Hello World!
```
If the model responds, the setup is correct.

---
### Step 5: Install Python Dependencies and Run GRAiS

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```
---

#### Run in Desktop Mode
Start the desktop application:
```bash
python desktop/main.py
```
---

#### Run in Web Mode
Start the web server:
```bash
python web/manage.py runserver
```