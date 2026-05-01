from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from openai import OpenAI

load_dotenv()


api=os.getenv("GEMINI_API_KEY")


embeddings_model = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-small-en-v1.5",
    huggingfacehub_api_token=os.environ["HF_TOKEN"],
)

vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_nodejs_with_rag",
    embedding=embeddings_model
)
client= OpenAI(
    api_key=api,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



user_query=input("Ask Something about nodejs: ")


result=vector_db.similarity_search(query=user_query)


count=0;

formatted_result=[]


count=0
for res in result:
    entry=(
        f"page content {res.page_content} \n"
        f"page number {res.metadata.get('page')} \n"
        f"source : {res.metadata.get('source')} \n"
    )

    formatted_result.append(entry)

context = "\n\n\n".join(formatted_result)





SYSTEM_PROMPT= f"""
    You are a helpful AI assistant who answers users query based on the available context retrieved from a pdf file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.
    {context}

"""


response=client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":user_query
        }
    ]
)

print(response.choices[0].message.content)