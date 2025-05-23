Offline AI Assistant
Overview
This project is an offline AI assistant that runs on your computer without needing the internet. It uses the Mistral 7B model to answer questions, follow custom rules, and remember past chats. You can train it to learn new responses, and it works faster with a GPU like the RTX 4070. The assistant has two interfaces: a command-line tool and a graphical web interface.
Features

Offline Operation: Works without internet for privacy.
Custom Rules: Set predefined responses in rules.txt (e.g., "Hello" → "Hi!").
Training: Teach new responses with commands like [TRAIN] hi → hello.
Memory: Remembers past chats using SQLite (chat_history.db) and FAISS (chat_index.faiss).
GPU Support: Optimized for NVIDIA GPUs (e.g., RTX 4070) with CUDA.
Graphical Interface: Web-based UI using Gradio.

System Requirements

Windows (tested on Windows 11 Pro)
16GB+ RAM (32GB recommended)
4GB+ storage for the model file
NVIDIA GPU (optional, for faster performance)
Python 3.12

Setup Instructions

Install Python 3.12:
Download from python.org.
Check "Add Python to PATH" during installation.


Install Git and Build Tools:
Git: git-scm.com
Visual Studio Build Tools (C++): visualstudio.microsoft.com
CMake: cmake.org


For GPU Support:
Install NVIDIA drivers: nvidia.com
Install CUDA Toolkit 12.1: developer.nvidia.com


Set Up Virtual Environment:
Open PowerShell and navigate to the project folder:cd path\to\project


Create and activate a virtual environment:py -3.12 -m venv ai_assistant_env
.\ai_assistant_env\Scripts\activate


If activation fails, run:Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned




Install Dependencies:
Run:pip install llama-cpp-python --extra-index-url https://download.pytorch.org/whl/cu121
pip install gradio sentence-transformers faiss-cpu numpy





Usage

Command-Line Interface:
Run:& "path\to\ai_assistant_env\Scripts\python.exe" "path\to\gpu_assistant.py"


Type commands like "Hello" or train with [TRAIN] hi → hello.


Graphical Interface:
Run:& "path\to\ai_assistant_env\Scripts\python.exe" "path\to\gui_gpu.py"


Open http://127.0.0.1:7860 in your browser if it doesn’t launch automatically.
Chat and upload rules via the web interface.



Files

rules.txt: Predefined rules (e.g., [COMMAND] Hello [RULE] Hi!)
data/: Stores chat_history.db (chat history) and chat_index.faiss (memory index)
mistral-7b-instruct-v0.1.Q4_K_M.gguf: AI model file
gpu_assistant.py: Command-line interface (GPU)
gui_gpu.py: Graphical interface (GPU)

Troubleshooting

GUI Not Opening: Modify gui_gpu.py to demo.launch(server_name='0.0.0.0', server_port=7860, inbrowser=True). Allow port 7860 in Windows Firewall.
Incomplete Responses: Increase max_tokens to 200 in gpu_assistant.py and gui_gpu.py.
Installation Errors: Ensure Python 3.12, Git, Build Tools, and CUDA match the system.

License
This project is for personal use by the client and not licensed for distribution.
