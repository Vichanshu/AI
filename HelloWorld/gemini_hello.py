from google import genai


client= genai.Client(
    api_key=""
)

response = client.models.generate_content(
    model="gemini-3-flash-preview" ,
    contents="Create a code for hello world in c"
)

print(response.text)