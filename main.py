# ✅ Setup OpenAI API Client
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import ollama_tools  # Assuming you defined tools for Ollama
from system_prompt import system_prompt


# ✅ Load environment variables
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# ✅ Initialize OpenAI (Ollama-compatible) client
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OPENAI_API_KEY,  # Required by SDK, even if ignored by Ollama backend
)

# ✅ Initialize conversation history
conversation_history = [
    {"role": "system", "content": system_prompt}
]

print("Chat started. Type 'exit' to quit.\n")


def main():
        
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # Append user message to conversation history
        conversation_history.append({"role": "user", "content": user_input + "/no_think" })

        # ✅ Send message to Ollama/OpenAI backend
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation_history,
            tools=ollama_tools,  # Optional: depends on whether your Ollama model uses tools
            tool_choice="auto",
            temperature=0.9,
        )

        # ✅ Extract and print assistant message
        message = response.choices[0].message.content
        print(f"Assistant: {message}\n")

        # ✅ Add assistant message to conversation history
        conversation_history.append({"role": "assistant", "content": message})

# ✅ Entry point guard
if __name__ == "__main__":
    main()