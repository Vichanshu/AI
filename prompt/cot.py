from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api=os.getenv("GEMINI_API_KEY")


client= OpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYS_PROMPT="""
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    -Strictly FOLLOW the given JSON output format
    -Only run one step at a time.
    -The sequence of steps is START(where user gives an input),PLAN(That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    {"step":"START" | "PLAN" | "OUTPUT" ,"content":"string"}

    EXAMPLE:
    START:Hey, can you solve 2+3*5/10
    PLAN:{"step":"PLAN" , "content":"Seems like user is interested in math problem"}
    PLAN:{"step":"PLAN" , "content":"looking at the problem , we should solve thsi using BODMAS method"}
    PLAN:{"step":"PLAN" , "content":"Yes, the BODMAS is correct thing to be done here"}
    PLAN:{"step":"PLAN" , "content":"first we must multiply 3*5 which is 15"}
    PLAN:{"step":"PLAN" , "content":"Now the equation is 2+15/10"}
    PLAN:{"step":"PLAN" , "content":"Now we should divide 15/10 which is 1.5"}
    PLAN:{"step":"PLAN" , "content":"Now the equation is 2+1.5"}
    PLAN:{"step":"PLAN" , "content":"Now finally lets perform the add which is 2+1.5 =3.5"}
    OUTPUT:{"step":"OUTPUT", "content": "3.5"}

"""


response=client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type":"json_object"},
    messages=[
        {
            "role":"system",
            "content":SYS_PROMPT
        },
        {
            "role":"user",
            "content":"find the answer of the equation x+3=10"
        },
        {
            "role":"assistant",
            "content":json.dumps({
                "step":"START",
                "content":"find the answer of the equation x+3=10"
            }
            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "PLAN", "content": "The user wants to solve the equation x+3=10."}

            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "PLAN", "content": "To solve for x, I need to isolate x on one side of the equation."}
            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "PLAN", "content": "I will subtract 3 from both sides of the equation to isolate x."}
            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "PLAN", "content": "x + 3 - 3 = 10 - 3"}
            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "PLAN", "content": "x = 7"}
            )
        },
        {
            "role":"assistant",
            "content":json.dumps(
                {"step": "OUTPUT", "content": "x = 7"}
            )
        }

    ]
)

print(response.choices[0].message.content)

