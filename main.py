from rag_chatbot import Chatbot

if __name__ == "__main__":
    
    bot = Chatbot()
    
    print("Competitive Programming Assistant")
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            response = bot.respond(user_input)
            print("\nBot:", response)
            print("\n" + "="*80 + "\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            continue