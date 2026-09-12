import ollama

history = []
model = 'qwen3-1.7b'

while True:
    prompt = input("You: ").strip()
    if prompt.lower() in ('exit','quit'):
        print("Have a nice day!")
        break
    
    message = {
        "role": "user",
        "content": prompt
    }

    history.append(message)
    response = ollama.chat(model=model,messages=history)
    bot_message_content = response.message.content
    print(f"Bot: {bot_message_content}")
    bot_message =  {
        "role": "assistant",
        "content": bot_message_content
    }
    history.append(bot_message)
