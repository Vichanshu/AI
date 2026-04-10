from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from huggingface_hub import InferenceClient
from huggingface_hub import InferenceClient
import os
from langchain_huggingface import HuggingFaceEndpointEmbeddings




from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
pdf_path =Path(__file__).parent / "node.pdf"

loader=PyPDFLoader(file_path=pdf_path)
docs =loader.load()

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)


chunks = text_splitter.split_documents(documents=docs)

# print(text[0])

embeddings_model = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-small-en-v1.5",
    huggingfacehub_api_token=os.environ["HF_TOKEN"],
)


vector_store= QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings_model,
    url="http://localhost:6333",
    collection_name="learning_nodejs_with_rag"
)


print("Indexing of documents done")



