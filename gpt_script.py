from dotenv import load_dotenv
import json
load_dotenv()  # take environment variables from .env.
from openai import OpenAI
client = OpenAI()

# Opening JSON file
f = open('chess.json')

# returns JSON object as
# a dictionary
data = json.load(f)
data = "1. d4 d5 2. c4 dxc4 3. e4 e5 4. Nf3 exd4 5. Qxd4 Qxd4 6. Nxd4"
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You are a chess game commentator. Share your views on the given chess board of the game being played and explain what's happening while highlighting the value of the latest move. The moves is given in the PGN format"
    },
    {
      "role": "user",
      "content": f"{data}"
    }
  ],
  temperature=0,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response.choices[0].message.content)