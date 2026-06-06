import gradio as gr
from groq import Groq
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Personas definition containing system prompts, few-shot examples, and formats
PERSONAS = {
    "Technical Explainer": {
        "system_prompt": (
            "You are a Technical Explainer. Your goal is to explain complex technical concepts "
            "in a clear, simple, and jargon-free manner. Avoid using advanced terms without explaining "
            "them first. Use relatable real-world analogies where possible."
        ),
        "few_shot_examples": [
            {
                "user": "What is an API?",
                "assistant": (
                    "Think of an API (Application Programming Interface) like a waiter in a restaurant. "
                    "You are the customer, and the kitchen is the system or database. Instead of going into the kitchen "
                    "yourself, you tell the waiter (the API) what you want to order. The waiter takes your request to the "
                    "kitchen, and then brings back your food (the data). It acts as a helpful messenger between two different systems."
                )
            },
            {
                "user": "How does encryption work?",
                "assistant": (
                    "Imagine sending a letter inside a locked box. You put the message in the box, lock it with a key, "
                    "and mail it. Even if someone steals the box along the way, they can't read the letter without the key. "
                    "When it reaches your friend, they use a matching key to unlock the box and read the message. In digital encryption, "
                    "the box is your data, and the keys are mathematical passwords."
                )
            }
        ],
        "output_format": "text"
    },
    "Debate Coach": {
        "system_prompt": (
            "You are a Debate Coach. For any question or topic presented, you must argue both sides "
            "of the issue fairly, objectively, and comprehensively. Structure your response by clearly presenting "
            "the arguments for (Pros) and arguments against (Cons), followed by a brief summary of how to balance these views."
        ),
        "few_shot_examples": [
            {
                "user": "Should artificial intelligence be regulated?",
                "assistant": (
                    "Here is a balanced debate on the regulation of Artificial Intelligence:\n\n"
                    "### Arguments for Regulation (Pros):\n"
                    "1. **Safety and Ethics**: Regulation prevents the creation of malicious autonomous systems and curbs deepfakes or misinformation.\n"
                    "2. **Job Security**: Policies can manage displacement of workers and ease transition periods.\n"
                    "3. **Bias Mitigation**: Audits ensure AI systems do not reinforce societal biases in hiring, lending, or policing.\n\n"
                    "### Arguments against Regulation (Cons):\n"
                    "1. **Stifling Innovation**: Too many restrictions can slow down groundbreaking technological research and economic competitiveness.\n"
                    "2. **Regulatory Lag**: Technology evolves far faster than legislation, making laws outdated before they are enacted.\n"
                    "3. **Decentralization Challenges**: Open-source projects and international boundaries make enforceability extremely difficult.\n\n"
                    "### Summary:\n"
                    "A balanced approach involves establishing flexible, principle-based guardrails that protect safety and privacy without placing heavy bureaucratic burdens on researchers and startups."
                )
            }
        ],
        "output_format": "text"
    },
    "Code Reviewer": {
        "system_prompt": (
            "You are an expert Code Reviewer. You must analyze the code snippet provided and return a structured feedback strictly in JSON format. "
            "The JSON must have the following keys: 'issues' (a list of strings representing identified issues), 'suggestions' (a list of strings representing actionable suggestions), "
            "and 'severity' (a single string containing 'Low', 'Medium', or 'High'). Do not include any explanation or markdown formatting outside the JSON."
        ),
        "few_shot_examples": [
            {
                "user": "def add(a, b):\n    return a+b",
                "assistant": (
                    '{"issues": ["No type hinting or docstring added."], '
                    '"suggestions": ["Add type hints for arguments and return value.", "Write a simple docstring explaining what the function does."], '
                    '"severity": "Low"}'
                )
            },
            {
                "user": "def get_user(id):\n    res = db.execute(f\'SELECT * FROM users WHERE id = {id}\')\n    return res.fetchone()",
                "assistant": (
                    '{"issues": ["SQL injection vulnerability due to string formatting in query.", "No error handling if database connection fails.", "No type annotations."], '
                    '"suggestions": ["Use parameterized queries instead of f-strings to prevent SQL injection.", "Wrap the execution block in a try-except block to handle DB errors.", "Add type hints to variables and functions."], '
                    '"severity": "High"}'
                )
            }
        ],
        "output_format": "json"
    },
    "Creative Writer": {
        "system_prompt": (
            "You are a Creative Writer. Write in a highly descriptive, vivid, and narrative-driven style. "
            "Use rich metaphors, sensory details, and an engaging tone to bring the description or story to life."
        ),
        "few_shot_examples": [
            {
                "user": "Describe a quiet library.",
                "assistant": (
                    "The library was a temple of silent thoughts, where the air smelled of aged paper, leather bindings, "
                    "and the quiet passage of time. Golden shafts of afternoon sun sliced through towering leaded windows, "
                    "illuminating dust motes that danced like tiny stars in a silent galaxy. Every footstep on the worn oak planks "
                    "was hushed, absorbed by rows of towering bookshelves that stood like ancient sentinels guarding the wisdom of centuries."
                )
            }
        ],
        "output_format": "text"
    }
}

def inject_few_shot(persona, user_query, history):
    """Prepends few-shot examples before actual user query in history."""
    messages = [{"role": "system", "content": persona["system_prompt"]}]
    
    # Prepend few-shot examples
    for example in persona["few_shot_examples"]:
        messages.append({"role": "user", "content": example["user"]})
        messages.append({"role": "assistant", "content": example["assistant"]})
        
    # Append conversation history
    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content")
        elif hasattr(msg, "role") and hasattr(msg, "content"):
            role = msg.role
            content = msg.content
        else:
            continue
            
        if role and content:
            # Extract string if content is a dictionary or object
            if isinstance(content, dict):
                content = content.get("text", "")
            elif not isinstance(content, str) and hasattr(content, "text"):
                content = content.text
                
            messages.append({"role": role, "content": str(content)})
            
    # Append actual user query
    final_query = user_query
    if persona["output_format"] == "json":
        final_query += "\n\nRemember: You must respond ONLY with a valid JSON object containing keys 'issues' (list of strings), 'suggestions' (list of strings), and 'severity' ('Low', 'Medium', or 'High'). Do not wrap your response in markdown code blocks."
        
    messages.append({"role": "user", "content": final_query})
    return messages

def bot_response(history, mode, temperature):
    """Handles chatbot completion with streaming responses."""
    if not history:
        yield history
        return
        
    persona = PERSONAS.get(mode, PERSONAS["Technical Explainer"])
    
    # We take all historical messages except the last one (which is the current user prompt)
    past_history = history[:-1]
    last_msg_obj = history[-1]
    
    # Extract raw user message
    if isinstance(last_msg_obj, dict):
        user_query = last_msg_obj.get("content", "")
    elif hasattr(last_msg_obj, "content"):
        user_query = last_msg_obj.content
    else:
        user_query = str(last_msg_obj)
        
    # Extract string if user_query is a dictionary or object
    if isinstance(user_query, dict):
        user_query = user_query.get("text", "")
    elif not isinstance(user_query, str) and hasattr(user_query, "text"):
        user_query = user_query.text
        
    # Inject few-shot examples
    messages = inject_few_shot(persona, user_query, past_history)
    
    # Call Groq API with streaming
    response_format = None
    if persona["output_format"] == "json":
        response_format = {"type": "json_object"}
        
    try:
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            stream=True,
            response_format=response_format
        )
    except Exception as e:
        yield history + [{"role": "assistant", "content": f"⚠️ Error calling API: {str(e)}"}]
        return
        
    accumulated = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        accumulated += delta
        
        # Special rendering for Code Reviewer (structured JSON)
        if persona["output_format"] == "json":
            try:
                # Clean up any potential markdown wrappers if the model generated them
                clean_text = accumulated.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
                
                data = json.loads(clean_text)
                
                # Format to structured markdown
                severity = data.get("severity", "Low").strip().capitalize()
                severity_badge = "🟢" if severity == "Low" else "🟡" if severity == "Medium" else "🔴"
                
                markdown_out = f"### 🔍 Code Review Report\n\n"
                markdown_out += f"**Severity Level:** {severity_badge} **{severity}**\n\n"
                
                markdown_out += "#### ⚠️ Issues Identified:\n"
                issues = data.get("issues", [])
                if isinstance(issues, list) and issues:
                    for issue in issues:
                        markdown_out += f"- {issue}\n"
                else:
                    markdown_out += "- No critical issues identified.\n"
                    
                markdown_out += "\n#### 💡 Suggestions:\n"
                suggestions = data.get("suggestions", [])
                if isinstance(suggestions, list) and suggestions:
                    for suggestion in suggestions:
                        markdown_out += f"- {suggestion}\n"
                else:
                    markdown_out += "- No specific suggestions.\n"
                    
                yield history + [{"role": "assistant", "content": markdown_out}]
            except Exception:
                # Show raw response with warning during parsing/incomplete stream
                yield history + [{"role": "assistant", "content": f"⚠️ *Parsing JSON Code Review...*\n\n{accumulated}"}]
        else:
            # Standard streaming text output
            yield history + [{"role": "assistant", "content": accumulated}]

with gr.Blocks() as demo:
    gr.Markdown("# PromptForge — Multi-Mode AI Assistant")
        
    with gr.Row():
        with gr.Column(scale=1):
            mode_dropdown = gr.Dropdown(
                choices=list(PERSONAS.keys()),
                value="Technical Explainer",
                label="Select AI Persona",
                interactive=True
            )
            temp_slider = gr.Slider(
                minimum=0.0,
                maximum=1.5,
                value=0.7,
                step=0.1,
                label="Temperature Control",
                interactive=True
            )
            
            with gr.Accordion("Active System Prompt", open=True):
                prompt_display = gr.Markdown(PERSONAS["Technical Explainer"]["system_prompt"])
                
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=500)
            
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Ask anything or enter code for review...",
                    show_label=False,
                    scale=4,
                    container=False
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
                
            clear_btn = gr.ClearButton([chatbot, msg_input], value="🗑️ Clear Chat", variant="secondary")

    # Hook up the prompt display update when changing the mode dropdown
    def on_mode_change(selected_mode):
        return PERSONAS[selected_mode]["system_prompt"]
        
    mode_dropdown.change(
        fn=on_mode_change,
        inputs=mode_dropdown,
        outputs=prompt_display
    )
    
    # Message submitting events
    def user_submit(message, history):
        # Extract string message if it's a dict or object
        text_message = message
        if isinstance(message, dict):
            text_message = message.get("text", "")
        elif not isinstance(message, str) and hasattr(message, "text"):
            text_message = message.text
            
        if not text_message or not str(text_message).strip():
            return "", history
            
        return "", history + [{"role": "user", "content": text_message}]
        
    msg_input.submit(
        fn=user_submit,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot],
        queue=False
    ).then(
        fn=bot_response,
        inputs=[chatbot, mode_dropdown, temp_slider],
        outputs=chatbot
    )
    
    send_btn.click(
        fn=user_submit,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot],
        queue=False
    ).then(
        fn=bot_response,
        inputs=[chatbot, mode_dropdown, temp_slider],
        outputs=chatbot
    )

if __name__ == "__main__":
    # Define a premium theme using Gradio's Python theme engine
    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="indigo",
        neutral_hue="slate"
    )
    demo.launch(inbrowser=True, theme=theme)