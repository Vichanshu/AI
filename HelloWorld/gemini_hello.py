from google import genai


client= genai.Client(
    api_key="AIzaSyDh6qdsXfw1rkPpcnOhX6DClCOT4E4IP0Y"
)

response = client.models.generate_content(
    model="gemini-3-flash-preview" ,
    contents="Create a code for hello world in c"
)

print(response.text)