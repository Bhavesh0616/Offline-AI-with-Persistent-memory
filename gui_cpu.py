import logging
import gradio as gr
from llama_cpp import Llama
from memory_manager import MemoryManager

# Suppress the "Could not find platform independent libraries <prefix>" warning
logging.getLogger().setLevel(logging.ERROR)

# Load LLM on CPU
llm = Llama(model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_gpu_layers=0, verbose=False)
print("LLM loaded on CPU successfully.")
mm = MemoryManager()
mm.load_rules("rules.txt")

# Function to process file upload
def process_file(file):
    if file is not None:
        if not file.endswith('.txt'):
            return "Invalid file type. Please upload a .txt file."
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            commands = [line.replace("[COMMAND]", "").strip() for line in lines if line.startswith("[COMMAND]")]
            rules = [line.replace("[RULE]", "").strip() for line in lines if line.startswith("[RULE]")]
            if len(commands) == len(rules):
                for cmd, rule in zip(commands, rules):
                    mm.save_chat(cmd, rule)
                return "Rules from file loaded successfully!"
            return "Invalid file format. Use [COMMAND] and [RULE] lines."
        except Exception as e:
            return f"Error reading file: {str(e)}"
    return "No file uploaded."

# Function to handle chat
def chat(message, history):
    if history is None:
        history = []

    rule_response = mm.get_rule_response(message)
    if rule_response:
        history.append(("You", message))
        history.append(("Assistant", rule_response))
        return history

    memory_results = mm.search_memory(message)
    if memory_results:
        history.append(("You", message))
        history.append(("Assistant", memory_results[0][1]))
        return history

    response = llm(f"Q: {message}\nA:", max_tokens=50)["choices"][0]["text"].strip()
    mm.save_chat(message, response)
    history.append(("You", message))
    history.append(("Assistant", response))
    return history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Offline AI Assistant with Gradio (CPU Version)")
    with gr.Row():
        with gr.Column():
            file_upload = gr.File(label="Upload Rules File (e.g., rules.txt)", type="filepath")
            upload_button = gr.Button("Process File")
            upload_output = gr.Textbox(label="Upload Status")
        with gr.Column():
            chatbot = gr.Chatbot(label="Chat with AI", height=500)
            msg = gr.Textbox(label="Your Message")
            submit_btn = gr.Button("Send")

    upload_button.click(fn=process_file, inputs=file_upload, outputs=upload_output)
    submit_btn.click(fn=chat, inputs=[msg, chatbot], outputs=chatbot).then(
        fn=lambda: gr.update(value=""), inputs=None, outputs=msg
    )

# Launch the interface and open browser automatically
demo.launch(server_name="127.0.0.1", server_port=7860, debug=True, inbrowser=True)
