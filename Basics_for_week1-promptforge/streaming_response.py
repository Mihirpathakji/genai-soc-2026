# import gradio as gr
# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def chat_stream(message, history):
#     messages = [{"role": "system", "content": "You are a helpful assistant."}]

#     # include conversation history
#     for human, bot in history:
#         messages.append({"role": "user",      "content": human})
#         messages.append({"role": "assistant", "content": bot})
#     messages.append({"role": "user", "content": message})

#     stream = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=messages,
#         stream=True,   # enables streaming
#     )

#     accumulated = ""
#     for chunk in stream:
#         delta = chunk.choices[0].delta.content or ""
#         accumulated += delta
#         yield accumulated   # update UI on each token


# # Launch the interface and force it to open up automatically!
# gr.ChatInterface(
#     fn=chat_stream,
#     title="My First AI Chat App",
# ).launch(inbrowser=True) 


#Code given in the MSOC material is failing for the repitive prompts.So i have made the AI chat app with following code which runs on repitive prompts also. 

import gradio as gr
from groq import Groq   
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_stream(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # FORCE-CLEAN HISTORY: Converts modern Gradio objects back into a simple list of [user, bot] strings
    clean_history = []
    for turn in history:
        # If it's a modern Gradio object, extract text. Otherwise, read it normally.
        user_msg = turn.get("content") if isinstance(turn, dict) else getattr(turn, "user", getattr(turn, "content", turn[0]))
        bot_msg = turn.get("content") if isinstance(turn, dict) else getattr(turn, "assistant", getattr(turn, "content", turn[1]))
        
        # Handle cases where the object has a .text attribute or is a list/tuple pair
        user_text = user_msg if isinstance(user_msg, str) else getattr(user_msg, "text", str(user_msg))
        bot_text = bot_msg if isinstance(bot_msg, str) else getattr(bot_msg, "text", str(bot_msg))
        
        clean_history.append([user_text, bot_text])

    # YOUR EXACT ORIGINAL LOOP (Now running safely over clean_history!)
    for human, bot in clean_history:
        messages.append({"role": "user",      "content": human})
        messages.append({"role": "assistant", "content": bot})
        
    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True,   # enables streaming
    )

    accumulated = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        accumulated += delta
        yield accumulated   # update UI on each token

# Launch the interface exactly how you wanted it!
gr.ChatInterface(
    fn=chat_stream,
    title="My First AI Chat App",
).launch(inbrowser=True)