from getpass import getpass
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

vectorstore = Chroma(persist_directory='db', embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chat = ChatOpenAI(
    openai_api_key = os.getenv("OPENAI_API_KEY"),
    model_name = "gpt-3.5-turbo",
    temperature = 0.0,
    max_tokens = 300,
)

# Create Prompt
template = """Use the following pieces of context to answer the question at the end.
Answers the question enthusiastically.
If the question is a greeting, answer cordially. 
If you don't know the answer, just say that you don't know.
Don't try to make up an answer.
{context}

Question: {question}
Answer Answer (write enthusiastically, write in summary): 
"""

PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm = chat,
    chain_type = "stuff",
    retriever = retriever,
    chain_type_kwargs={"prompt": PROMPT},
    verbose=True
)

text_invalid_response = [
    "No sé.",
    "don't know",
    "I don't understand"
]

def chat(prompt):
    response = qa_chain(prompt)
    return validate_response(response["result"])

def validate_response(response):
    for text in text_invalid_response:
        if text in response:
            return "Estimado/a cliente,\n\nLamentamos no poder proporcionar una respuesta precisa a su pregunta en este momento. nos encantaria poder reunirnos y aclarar tus dudas, agenda una réunion con nosotros en el siguiente enlace y con mucho gusto te atenderemos: https://calendly.com/tuterrenoenusa/30min"
            break
    return response

""" while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = chat(text_input)
    print(response) """