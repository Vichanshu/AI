from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api=os.getenv("GEMINI_API_KEY")


client= OpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYS_PROMPT="You should only answer questions related to coding only , in all other cases just say sorry!"


response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role":"system",
            "content":SYS_PROMPT
        },
        {
            "role":"user",
            "content":"Hello can you tell me a joke on a boy named sujal"
        }
    ]
)

print(response.choices[0].message.content)

#Zero Shot prompting: The model is given direct question or task without any prior examples.