
# from openai import OpenAI
import os
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(
#     api_key=os.environ.get("GROQ_API_KEY"),
#     base_url="https://api.groq.com/openai/v1",
# )

# response = client.responses.create(
#     input="Explain the importance of fast language models",
#     model="llama-3.3-70b-versatile",
# )
# print(response.output_text)


def run_command(cmd:str):
    res=os.system(cmd)
    return res


print(run_command("h"))
