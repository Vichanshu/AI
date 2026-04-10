import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


api=os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {"role":"user", "content":"Hello my name is Sujal , how are you?"}
    ]
)

print(response.choices[0].message.content)