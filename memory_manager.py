import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class MemoryManager:
    def __init__(self, db_path="chat_history.db", index_path="chat_index.faiss"):
        """Initialize SQLite database and FAISS index."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chats 
                            (id INTEGER PRIMARY KEY, user_input TEXT, response TEXT, timestamp TEXT)''')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Check if index file exists, read or create new
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.rules = {}

    def save_chat(self, user_input, response):
        """Save conversation to SQLite and update FAISS index."""
        timestamp = "2025-04-24"
        self.cursor.execute("INSERT INTO chats (user_input, response, timestamp) VALUES (?, ?, ?)",
                           (user_input, response, timestamp))
        self.conn.commit()
        embedding = self.model.encode([user_input])
        self.index.add(embedding)
        faiss.write_index(self.index, "chat_index.faiss")

    def search_memory(self, query):
        """Search FAISS index for similar past inputs."""
        embedding = self.model.encode([query])
        distances, indices = self.index.search(embedding, k=5)
        results = []
        for idx in indices[0]:
            if idx >= 0:
                self.cursor.execute("SELECT user_input, response FROM chats WHERE id=?", (idx,))
                result = self.cursor.fetchone()
                if result:
                    results.append(result)
        return results

    def load_rules(self, file_path):
        """Load rules from file using file_processor."""
        from file_processor import process_file
        self.rules = process_file(file_path)

    def get_rule_response(self, user_input):
        """Check if user input matches a command and return rule response."""
        for cmd in self.rules.get("COMMAND", []):
            if cmd.lower() in user_input.lower():
                idx = self.rules.get("COMMAND", []).index(cmd)
                rule = self.rules.get("RULE", [])[idx] if idx < len(self.rules.get("RULE", [])) else None
                return rule.strip() if rule else None
        return None

    def __del__(self):
        """Close database connection on object deletion."""
        self.conn.close()

# Test the class
if __name__ == "__main__":
    mm = MemoryManager()
    mm.load_rules("rules.txt")  # Use sample_rules.txt as per our adjustment
    mm.save_chat("hello", "hi there")
    print("Memory Search:", mm.search_memory("hello"))
    print("Rule Response:", mm.get_rule_response("greet"))