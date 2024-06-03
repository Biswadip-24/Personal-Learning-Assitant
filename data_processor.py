import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from PyPDF2 import PdfReader
import prompts as pt
import ast 

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()
model = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME"), 
    google_api_key=os.getenv("GOOGLE_API_KEY"), 
    temperature=0
)

embedding_model = "models/embedding-001"
faiss_index = "faiss_index_pla"

def generate_documents(file):
    document = PdfReader(file)

    text = ""
    for page in document.pages:
        text += page.extract_text()

    splitter = RecursiveCharacterTextSplitter(chunk_size=4000)
    doc_chunks = splitter.create_documents([text])
    return doc_chunks

def create_vector_db(documents):
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    vectordb = FAISS.from_documents(documents, embedding=embeddings)
    vectordb.save_local(faiss_index)

def generate_questions(file):
    documents = generate_documents(file)
    create_vector_db(documents)

    chain = load_summarize_chain(
        llm=model,
        chain_type="refine",
        refine_prompt=pt.refine_prompt,
        question_prompt=pt.question_prompt,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_list",
    )

    result = chain({"input_documents": documents})
    questions = result["output_list"]  
    # print(questions)

    # convert dict to list
    # question_lists = questions[1]
    # print(type(questions))

    questions = questions[questions.index("["):questions.index("]")+1]

    question_list = ast.literal_eval(questions) 
    # print(questions)

    # question_list = []

    return question_list

def get_question_answer(question):
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
    db = FAISS.load_local(faiss_index, embeddings=embeddings,allow_dangerous_deserialization=True)

    chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=db.as_retriever()
    )

    response = chain({"question":question, "chat_history":[]})
    return response["answer"]

def get_answers(questions):
    answers = []
    for question in questions:
        answer = get_question_answer(question)
        answers.append(answer)
    
    return answers