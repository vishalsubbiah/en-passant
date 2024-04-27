from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from openai import OpenAI
from collections import deque

class ChatApp:
    def __init__(self, conv_limit=10, model="gpt-3.5-turbo", persona=None, persona_freq=3):
        self.client = OpenAI()
        self.persona = persona
        self.persona_spot=-1
        self.prompt = self.get_prompt()
        self.base_message = {
            "role": "system",
            "content": self.prompt
        }
        self.messages_queue = deque(maxlen=conv_limit)
        self.move_count=1
        self.all_responses = []
        self.persona_options = ["Gordon Ramsey from Hell's Kitchen", "Magnus Carlson", "Aziz Ansari from Parks and Rec", "Ron Swanson from Parks and Rec"]

        if self.persona is None:
            self.persona = self.persona_options[0]
            self.persona_spot = 0
        self.num_personas = len(self.persona_options)
        self.persona_freq=persona_freq

    def chat(self, message):
        if self.move_count%self.persona_freq==0:
            # redo prompt with a new persona
            self.persona_spot+=1
            self.change_persona(
                self.persona_options[self.persona_spot%self.num_personas]
            )
        self.messages_queue.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[self.base_message, *self.messages_queue],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response.choices[0].message.content
        self.messages_queue.append({"role": "assistant", "content": output})
        self.move_count+=1
        self.all_responses.append(output)
        return f"move: {message}, {self.persona}: {output}"

    def get_prompt(self):
        return f"You are a chess game commentator. Share your views on the given chess board of the game being played and explain what's happening with a focus on the latest move. Explain how good or bad the last move is and what is the best way for the opponent to respond to it. Communicate the information similar to how {self.persona} would. The moves is given in the PGN format"

    def change_persona(self, persona):
        self.persona = persona
        self.base_message["content"] = self.get_prompt()


chat_app = ChatApp()
entries = [
    "1. d4",
    "1. d4 d5",
    "1. d4 d5 2. c4",
    "1. d4 d5 2. c4 dxc4",
    "1. d4 d5 2. c4 dxc4 3. e4",
    "1. d4 d5 2. c4 dxc4 3. e4 e5",
    "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3",
    "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3 exd4",
    "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3 exd4 5. Qxd4",
    "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3 exd4 5. Qxd4 Qxd4",
    "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3 exd4 5. Qxd4 Qxd4 6. Nxd4"
    ]
for entry in entries:
    response = chat_app.chat(entry)
    print(f"{response}\n\n")
