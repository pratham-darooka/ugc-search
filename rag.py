from globals import DIRECTORY, GOOGLE_API_KEY
from prompts import RAG_GENERATOR, REDDIT_RAG_GENERATOR, YT_RAG_GENERATOR
from langchain_google_genai import (ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings,HarmBlockThreshold,
    HarmCategory,)
from logger import logger
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def predict(question, vector_index, prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro-latest",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5,
        convert_system_message_to_human=True,
        safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
    )

    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query":question})
    return result["result"]

def loading_content():
    jq_schema = '.'
    chunks = []

    # Iterate through all files in the directory
    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".json"):  # Assuming all files are JSON files
            file_path = os.path.join(DIRECTORY, filename)
            json_loader = JSONLoader(file_path=file_path, jq_schema=jq_schema, text_content=False)

            # Load and split the JSON file
            single_post_chunks = json_loader.load_and_split()

            # Process the chunks as needed
            chunks.extend(single_post_chunks)

    return chunks


def chunking():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    context = "\n\n".join(str(p.page_content) for p in loading_content())
    texts = text_splitter.split_text(context)
    return texts, context


def init_vectorstore(texts):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":10})

    return vector_index


def search(user_request):
    logger.info("Performing RAG")
    logger.debug("Loading and Chunking posts")
    texts, context = chunking()
    logger.debug("Indexing posts")
    vector_index = init_vectorstore(texts)
    logger.info("Generating answer")
    answer = predict(user_request, vector_index, RAG_GENERATOR)
    return answer

def search_ytb(user_request):
    logger.info("Performing RAG")
    logger.debug("Loading and Chunking posts")
    texts, context = chunking()
    logger.debug("Indexing posts")
    vector_index = init_vectorstore(texts)
    logger.info("Generating answer")
    answer = predict(user_request, vector_index, YT_RAG_GENERATOR)
    return answer

def search_rddt(user_request):
    logger.info("Performing RAG")
    logger.debug("Loading and Chunking posts")
    texts, context = chunking()
    logger.debug("Indexing posts")
    vector_index = init_vectorstore(texts)
    logger.info("Generating answer")
    answer = predict(user_request, vector_index, REDDIT_RAG_GENERATOR)
    return answer