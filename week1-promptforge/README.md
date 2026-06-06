# PromptForge — Multi-Mode AI Assistant

> **Week 1 Project | GenAI Summer of Code 2026**  
> Built with 🐍 Python · 🤖 Groq Cloud API · 🎛️ Gradio Blocks

---

## 📌 What is PromptForge?

**PromptForge** is a multi-persona AI chatbot that lets you pick from 4 different AI modes, each with its own personality, behavior, and output style. Every mode uses a different **system prompt** and **few-shot examples** to guide the AI's responses — all powered by **Llama-3.3-70b-versatile** running on Groq's ultra-fast inference engine with **real-time token-by-token streaming**.

---

## 🚀 Live Demo (Run Locally)

```bash
# Step 1 — Clone the repo
git clone https://github.com/Mihirpathakji/genai-soc-2026.git
cd genai-soc-2026/week1-promptforge

# Step 2 — Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Step 3 — Install dependencies
pip install -r requirements.txt

# Step 4 — Add your Groq API Key
copy .env.example .env
# Open .env and replace with your actual key from https://console.groq.com

# Step 5 — Run the app
python app.py
```

The app will automatically open in your **default web browser** at `http://127.0.0.1:7860`

---

## 🎭 The 4 AI Personas

### 1. 📖 Technical Explainer
Explains any complex technical concept in a simple, jargon-free way using real-world analogies.

**Example Question:**
> *"What is Docker and containerization, and why do developers use it?"*

**Response Style:** Clear, beginner-friendly, uses everyday metaphors

---

### 2. ⚖️ Debate Coach
For any topic or question, the AI argues **both sides** fairly — presenting clear Pros and Cons followed by a balanced summary.

**Example Question:**
> *"Should cryptocurrency replace traditional paper currency globally?"*

**Response Style:** Structured Pros/Cons list with a concluding summary

---

### 3. 🔍 Code Reviewer
Paste any code snippet (Python, JavaScript, SQL, C++) and receive structured feedback rendered as a formatted **Code Review Report** with:
- Severity level 🟢 Low / 🟡 Medium / 🔴 High
- List of identified issues
- Actionable suggestions to fix them

**Example Input:**
```python
def read_file(filename):
    f = open(filename, "r")
    data = f.read()
    return data
```

**Response Style:** Structured Markdown report (parsed from JSON output)

---

### 4. ✍️ Creative Writer
Responds in a vivid, descriptive, and deeply narrative style — full of metaphors, sensory details, and immersive storytelling.

**Example Question:**
> *"Describe a bustling futuristic marketplace on a distant planet at sunset."*

**Response Style:** Rich prose with vivid imagery and descriptive language

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core language |
| **Gradio Blocks** | Web UI framework (no HTML/CSS needed) |
| **Groq Cloud API** | Ultra-fast LLM inference |
| **Llama-3.3-70b-versatile** | Language model powering all 4 personas |
| **python-dotenv** | Secure API key loading from `.env` file |

---

## 🔑 Key Concepts Used

### 1. System Prompts
Each persona has a unique system prompt that tells the AI **who it is** and **how to behave**. This is the first message sent in every conversation.

### 2. Few-Shot Examples
Before each user message, we inject pre-written example conversations for the selected persona. This teaches the model the **exact tone, format, and style** to use — without needing to fine-tune.

### 3. Streaming Responses
We use `stream=True` in the Groq API call, which returns text **token by token**. Gradio's `yield` generator pattern re-renders the chat bubble on every token — creating the live typing effect.

### 4. Temperature Control
A slider from `0.0` to `1.5` controls the **creativity/randomness** of responses:
- `0.0` — Precise, consistent, factual
- `0.7` — Balanced (default)
- `1.5` — Creative, exploratory, unpredictable

### 5. JSON Rendering (Code Reviewer)
When Code Reviewer mode is active, the API is forced to respond in valid JSON. We parse this JSON and render it as a clean, structured Markdown **Code Review Report** with severity badges and bullet-point lists.

---

## 📁 Project Structure

```
week1-promptforge/
│
├── app.py              # Main application — all logic, personas, and UI
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API key (no real keys)
├── .env                # Your actual API key (gitignored, never pushed)
└── README.md           # This file
```

---

## 📦 Requirements

```
groq
gradio
python-dotenv
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the `week1-promptforge/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at: **https://console.groq.com**

> ⚠️ **Never commit your `.env` file to GitHub.** It is listed in `.gitignore` to protect your secret key.

---

## ✅ Deliverables Checklist

- [x] `app.py` — Working Gradio app with 4 personas
- [x] `requirements.txt` — All dependencies listed
- [x] `.env.example` — Template file with no real key
- [x] `README.md` — Full documentation with setup instructions
- [x] Streaming responses implemented with `stream=True`
- [x] Few-shot injection for all 4 personas
- [x] JSON rendering for Code Reviewer mode
- [x] Temperature slider (0.0 – 1.5)
- [x] Active System Prompt accordion display

---

## 👤 Author

**Mihir Pathak**  
GenAI Summer of Code 2026  
GitHub: [@Mihirpathakji](https://github.com/Mihirpathakji)
