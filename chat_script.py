from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from openai import OpenAI
from groq import Groq
from collections import deque
import os

class ChatApp:
    def __init__(
            self,
            conv_limit=30,
            model="gpt-4o",
            client="openai",
            persona=None,
            persona_freq=2
        ):
        clients = {
            "openai" : OpenAI(),
            "groq": Groq(api_key=os.environ.get("GROQ_API_KEY"))
        }
        
        self.conv_limit = conv_limit
        self.model = model
        self.client = clients[client]
        self.persona = persona
        self.persona_spot=-1

        self.messages_queue = deque(maxlen=self.conv_limit)
        self.move_count=1
        self.all_responses = []
        self.persona_options = [
            "Gordon Ramsey",
            "Aziz Ansari",
            # "Ron Swanson",
            # "Magnus Carlson",
        ]

        if self.persona is None:
            self.persona = self.persona_options[0]
            self.persona_spot = 0
        self.prompt = self.get_prompt()
        self.base_message = {
            "role": "system",
            "content": self.prompt
        }
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
            model=self.model,
            messages=[self.base_message, *self.messages_queue],
            temperature=0.7,
            max_tokens=128,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response.choices[0].message.content
        self.messages_queue.append({"role": "assistant", "content": output})
        self.move_count+=1
        self.all_responses.append(output)
        return message, self.persona, output

    def get_prompt(self):
        prompt = f"You are a chess game commentator. Commentate in the voice of {self.persona}. The voice is very important. Share your views on the given chess board of the game being played and explain what's happening with a focus on the latest move. Explain how good or bad the last move is and what is the best way for the opponent to respond to it. Be consice with the message and not more than two sentences. The moves is given in the PGN format"
        # print(prompt)
        return prompt

    def change_persona(self, persona):
        self.persona = persona
        self.base_message["content"] = self.get_prompt()

if __name__ == "__main__":
    chat_app = ChatApp()
    entries = [
        "1. e4",
        "1. e4 e5",
        "1. e4 e5 2. Qh5",
        "1. e4 e5 2. Qh5 d6",
        "1. e4 e5 2. Qh5 d6 3. Bc4",
        "1. e4 e5 2. Qh5 d6 3. Bc4 Nf6",
        "1. e4 e5 2. Qh5 d6 3. Bc4 Nf6 4. Qxf7#"
    ]

    for entry in entries:
        response = chat_app.chat(entry)
        print(f"{response}\n\n")
