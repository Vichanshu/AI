from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
from pydantic import BaseModel,Field
from typing import Optional
from groq import Groq


load_dotenv()

client=OpenAI(
   api_key=os.getenv("GROQ_API_KEY"),
   base_url="https://api.groq.com/openai/v1"
)

SYS_PROMPT="""
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN ,TOOL, OBSERVE and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    While planning you can look upon the list of tools available if they can be used to give the desired output.
    for every tool wait for the observe step which is the output from the called tool.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    -Strictly FOLLOW the given JSON output format
    -Only run one step at a time.
    -The sequence of steps is START(where user gives an input),PLAN(That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    {"step":"START" | "PLAN" | "OUTPUT" | "TOOL"|"OBSERVE" ,"content":"string","input":"string" ,"tool":"string"}

    Available Tools:
    -get_weather(city:str): Takes city name as an input string and returns the weather info about the city

    EXAMPLE 1:
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



    EXAMPLE 2:
    START:What is the weather of Delhi?
    PLAN:{"step":"PLAN" , "content":"Seems like user is interested in getting the weather of Delhi in India"}
    PLAN:{"step":"PLAN" , "content":"Let's see if we have avialble tool from the lsit of available tools"}
    PLAN:{"step":"PLAN" , "content":"Great, we have get_weather tool available for this query."}
    PLAN:{"step":"PLAN" , "content":"I need to call get_weather tool available for delhi as input for city"}
    PLAN:{"step":"TOOL"  ,"tool":"get_weather", "input":"delhi"}
    PLAN:{"step":"OBSERVE" ,"tool":"get_weather","input":"delhi", "output":"The weather in Delhi is cloudy +24°C"}
    PLAN:{"step":"PLAN" , "content":"Oh great! I got the weather info about delhi"}
    OUTPUT:{"step":"OUTPUT", "content": "The current weather in delhi is 24°C with clody sky"}



"""


class MyOutputFormat(BaseModel):
    step:str=Field(...,description="The ID of the step. Example:PLAN,TOOL,OUTPUT")
    content:Optional[str]=Field(None,description="Optional content about the step")
    tool:Optional[str]=Field(None,description="The ID of the tool to call")
    input:Optional[str]=Field(None,description="Input for the tool to be called")




def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t&m"
    response = requests.get(url)
    if response.status_code==200:
        return f"The weather in {city} is {response.text}"
    else:
        return f"something went wrong"




Available_Tools={
    "get_weather":get_weather
}



message_history=[
    {"role":"system","content":SYS_PROMPT},
]

user_input=input("Hey how can i help you?\n")
message_history.append({"role":"user","content":user_input})



while True:
    response=client.chat.completions.parse(
        model="moonshotai/kimi-k2-instruct-0905",
        response_format=MyOutputFormat,
        messages=message_history
    )
    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant", "content":raw_result})

    parsed_result=response.choices[0].message.parsed


    if parsed_result.step=="START":
        print("llm has been started\n", parsed_result.content)
        continue

    if parsed_result.step=="PLAN":
        print("llm thinking\n",parsed_result.content)
        continue

    if parsed_result.step=="TOOL":
        tool_touse=parsed_result.tool
        tool_input=parsed_result.input
        tool_output=Available_Tools[tool_touse](tool_input)
        message_history.append({"role":"developer","content":json.dumps({"step":"OBSERVE","tool":tool_touse,"input":tool_input,"output":tool_output})})
        continue



    if parsed_result.step=="OUTPUT":
        print("final answer\n",parsed_result.content)
        break




