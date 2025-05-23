def process_file(file_path):
    commands = []
    rules = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("[COMMAND]"):
                    commands.append(line.replace("[COMMAND]", "").strip())
                elif line.startswith("[RULE]"):
                    rules.append(line.replace("[RULE]", "").strip())
        # Ensure commands and rules lists are aligned (same length)
        if len(commands) != len(rules):
            print("Warning: Number of commands and rules mismatch. Using the shorter list.")
            min_length = min(len(commands), len(rules))
            commands = commands[:min_length]
            rules = rules[:min_length]
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please ensure the file exists.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return {"COMMAND": commands, "RULE": rules}

if __name__ == "__main__":
    rules = process_file("rules.txt")
    print(f"Extracted Rules: {rules}")