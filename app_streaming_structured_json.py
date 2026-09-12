import ollama
import json

todos = []
history = []
model = 'qwen3-1.7b'

while True:
    prompt = input("You: ").strip()
    if prompt.lower() in ('exit','quit'):
        print("Have a nice day!")
        break
    
    if prompt.startswith("/todos"):
        print("bot:")
        if not todos:
            print("No tasks yet")
        else:
            for i,task in enumerate(todos):
                print(f"{i+1}. {task["text"]} by {task["due"]}")
        continue

    if prompt.startswith("/json"):
        sym_message = {
            "role": "system",
            "content": """EXTRACT the tasks and their due date/timings from user prompt... REPLY only with json with the exact format as: 
            {"tasks": [{"text": "", "due": ""}]}"""
        }
        message = {
            "role": "user",
            "content": prompt[len('/json'):].strip()
        }
        print("bot:",end="",flush=True)
        bot_message_content = ""
        response = ollama.chat(model=model,messages=[sym_message,message],format='json') #streaming avoided here
        try:
            reply = json.loads(response.message.content)
        except json.JSONDecodeError:
            print("Couldn't parse model response:")
            print(response.message.content)
            continue
        tasks = reply.get("tasks") if isinstance(reply,dict) else None
        if not isinstance(tasks,list):
            print("unexpected shape:",reply)
            continue
        

        for t in tasks:
            if not isinstance(t,dict):
                continue
            text = str(t.get("text","")).strip()
            if text:
                todos.append({"text": text,"due":t.get("due")})
        print()
        for i,task in enumerate(tasks):
            print(f"{i+1}. {task["text"]}, by due:{task["due"]}")
        continue

        
    message = {
        "role": "user",
        "content": prompt
    }

    history.append(message)
    print("Bot:",end ="",flush=True) #explain


    bot_message_content = ""
    response = ollama.chat(model=model,messages=history,stream=True)

    for chunk in response:
        bot_message_content += chunk.message.content
        print(chunk.message.content,end="",flush=True)
    print()
    #print(f"Bot: {bot_message_content}")
    bot_message =  {
        "role": "assistant",
        "content": bot_message_content
    }
    history.append(bot_message)
