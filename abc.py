from google import genai

client = genai.Client(api_key="AIzaSyDI7eBAFpQ5O9fNs_n-BKExJv6q9UJtqV4")
chat = client.chats.create(model="gemini-2.5-flash")

print("Gemini Q&A Chat - Type 'exit' to quit\n")

while True:
    # Get user question
    question = input("You: ")
    
    # Check if user wants to exit
    if question.lower() in ['exit', 'quit', 'bye']:
        print("\nChat History:")
        print("-" * 50)
        for message in chat.get_history():
            role = "You" if message.role == "user" else "Gemini"
            print(f"{role}: {message.parts[0].text}")
        print("\nGoodbye!")
        break
    
    # Send message and get response
    print("Gemini: ", end="")
    response = chat.send_message_stream(question)
    for chunk in response:
        print(chunk.text, end="")
    print("\n")