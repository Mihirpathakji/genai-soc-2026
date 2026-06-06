# PromptForge — Multi-Mode AI Assistant

A high-performance, multi-persona AI chatbot built with **Gradio Blocks** and the **Groq Cloud API** (running Llama-3.3-70b-versatile). The app features streaming outputs, dynamic few-shot injection, temperature control, and formatted markdown rendering for code reviews.

## Features

- **Selectable AI Personas**:
  - 📖 **Technical Explainer**: Translates complex tech jargon into simple concepts and analogies.
  - ⚖️ **Debate Coach**: Provides balanced perspective on controversial arguments (Pros/Cons).
  - 🔍 **Code Reviewer**: Analyzes syntax, lists vulnerabilities/suggestions, and rates severity (Low/Medium/High) by parsing structured JSON output.
  - ✍️ **Creative Writer**: Crafts rich, narrative-driven descriptions.
- **Few-Shot Injector**: Ensures context-appropriate formatting by prepending historical templates before user queries.
- **Interactive UI**:
  - Sidebar for Mode Selection and Temperature settings.
  - Collapsible system prompt accordion.
  - Clean chat container, Send button, and Clear history option.
- **Premium Design**: Built using modern dark theme styling, custom gradients, and a glassmorphic aesthetic.

## Setup Instructions

1. **Clone/Navigate to the directory**:
   ```bash
   cd week1-promptforge
   ```

2. **Configure your API Key**:
   Create a `.env` file in the root directory (based on `.env.example`) and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install Dependencies**:
   Ensure you have virtual environment active or install globally:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
