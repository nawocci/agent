from model import GeminiModel

def main():
    print("Type 'quit' or 'exit' to end the conversation\n")
    
    try:
        # Initialize the Gemini model
        gemini = GeminiModel()
        print()
        
        while True:
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Get response from Gemini
            response = gemini.generate_text(user_input)
            print(f"Gemini: {response}\n")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()