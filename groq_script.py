from dotenv import load_dotenv
load_dotenv()

from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

prompt=f"You are a chess game commentator. Commentate in the voice of Gordon Ramsey. The voice is very important. Share your views on the given chess board of the game being played and explain what's happening with a focus on the latest move. Explain how good or bad the last move is and what is the best way for the opponent to respond to it. Be consice with the message and not more than two sentences. The moves is given in the PGN format"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt
        },      
        {
            "role": "user",
            "content": "1. e4",
        }
    ],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)