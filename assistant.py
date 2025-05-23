import logging
from llama_cpp import Llama
from memory_manager import MemoryManager

# Suppress the "Could not find platform independent libraries <prefix>" warning
logging.getLogger().setLevel(logging.ERROR)

# Load LLM on CPU with reduced verbosity
llm = Llama(
    model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_gpu_layers=0,
    offload_kqv=True,
    verbose=False  # This disables most of the model loading logs
)
print("LLM loaded on CPU successfully.")

# Initialize memory manager
mm = MemoryManager()
mm.load_rules("rules.txt")

# Interaction loop
print("AI Assistant started. Type '[TRAIN] rule' to train, or anything to chat. 'exit' to quit.")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        break
    elif user_input.startswith("[TRAIN]"):
        rule = user_input.replace("[TRAIN]", "").strip()
        mm.save_chat(user_input, rule)
        print("Rule saved!")
    else:
        # Check rules first
        rule_response = mm.get_rule_response(user_input)
        if rule_response:
            print("Rule Response:", rule_response)
        else:
            # Check memory
            memory_results = mm.search_memory(user_input)
            if memory_results:
                print("Memory Response:", memory_results[0][1])
            else:
                # Generate with LLM on CPU
                response = llm(f"Q: {user_input}\nA:", max_tokens=50)["choices"][0]["text"].strip()
                print("LLM Response:", response)
                mm.save_chat(user_input, response)

print("Assistant stopped.")