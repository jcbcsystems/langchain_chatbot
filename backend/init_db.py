from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()

loader = PyPDFDirectoryLoader("docs/")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overload=200, 
    length_funcion=len,
    #separator = '.\n'
)

all_splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(
    documents=all_splits, 
    embedding=OpenAIEmbeddings(),
    persist_directory='db'
)

vectorstore.persist()
vectorstore = None