import logging
from llama_cpp import Llama
from memory_manager import MemoryManager

# Suppress the "Could not find platform independent libraries <prefix>" warning
logging.getLogger().setLevel(logging.ERROR)

# Load LLM on RTX 4070 GPU with optimized layers
llm = Llama(
    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_gpu_layers=40,  # Adjust based on RTX 4070 VRAM (12GB)
    offload_kqv=True,  # Offload key/query/value tensors to GPU
    verbose=False
)
print("LLM loaded on RTX 4070 GPU successfully.")

# Initialize memory manager
mm = MemoryManager()
mm.load_rules("rules.txt")

# Interaction loop
print("AI Assistant started. Type '[TRAIN] input → response' to train, or anything to chat. 'exit' to quit.")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break
    elif user_input.lower().startswith("[train]"):
        rule = user_input[len("[TRAIN]"):].strip()
        if "→" not in rule:
            print("Invalid training format. Use [TRAIN] input → response.")
            continue
        try:
            input_part, response_part = rule.split("→", 1)
            input_part = input_part.strip()
            response_part = response_part.strip()
            if not input_part or not response_part:
                print("Invalid training format. Both input and response must be non-empty.")
                continue
            mm.save_chat(input_part, response_part)
            print("Rule saved!")
        except Exception as e:
            print(f"Error saving rule: {e}")
    else:
        rule_response = mm.get_rule_response(user_input)
        if rule_response:
            print("Rule Response:", rule_response)
        else:
            memory_results = mm.search_memory(user_input)
            if memory_results:
                print("Memory Response:", memory_results[0][1])
            else:
                response = llm(f"Q: {user_input}\nA:", max_tokens=50)["choices"][0]["text"].strip()
                print("LLM Response:", response)
                mm.save_chat(user_input, response)

print("Assistant stopped.")