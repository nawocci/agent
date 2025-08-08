from model import GeminiModel
from interpreter import CommandInterpreter


def main():
    print("🤖 Gemini Chatbot with Commands")
    print("Type 'quit' or 'exit' to end the conversation\n")

    try:
        interpreter = CommandInterpreter()
        system_prompt = interpreter.get_system_prompt()
        gemini = GeminiModel(system_prompt)

        # Show discovered commands for quick verification
        available = ", ".join(interpreter.get_available_commands()) or "(none)"
        print(f"Available commands: {available}\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not user_input:
                continue

            response = gemini.generate_text(user_input)
            final_response = interpreter.execute_commands(response)
            print(f"Gemini: {final_response}\n")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()