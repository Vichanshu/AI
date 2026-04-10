from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api=os.getenv("GEMINI_API_KEY")


client= OpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYS_PROMPT="""
You should only answer questions related to coding only , in all other cases just say sorry!

Examples:
Q:Can you explain the a+b whole square?
A:Sorry! I can answer only coding questions.

Q:Hey, Write a code in python for adding two numbers
A:def add (a,b):
    return a+b

"""


response=client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system",
            "content":SYS_PROMPT
        },
        {
            "role":"user",
            "content":"Write a code to print hello world "
        }
    ]
)

print(response.choices[0].message.content)

