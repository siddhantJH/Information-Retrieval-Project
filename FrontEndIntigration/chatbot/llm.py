
import pandas as pd
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
# from langchain.chains import RetrievalQA
from langchain import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
Gemini_pro_llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                        google_api_key="AIzaSyBSaMUOmN4usfGXD9PT7OmDcCFCa9WvBMc",
                                        temperature=0.0,
                                        convert_system_message_to_human=True,
                                        safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    })

from langchain_google_genai import GoogleGenerativeAIEmbeddings
GeminiEmbeddingModel = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key="AIzaSyBSaMUOmN4usfGXD9PT7OmDcCFCa9WvBMc")
df = pd.read_csv('football_data_with_summary_V2.0.csv')
headingsList = df["content"].tolist()
tokenized_corpus = [doc.split(" ") for doc in headingsList]
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

document_retrieval_chain = create_stuff_documents_chain(Gemini_pro_llm, prompt)
from langchain.chains import create_retrieval_chain
from rank_bm25 import BM25Okapi
import gradio as gr
# # "What are the Requirements for M.tech Specialization. ?"
bm25 = BM25Okapi(tokenized_corpus)
def ask_Query(query):
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)

    a = bm25.get_top_n(tokenized_query, headingsList, n=2)
    # a[0] = "Sport as a Symbol of National Power" # hardcoded
    # resultContent = df.loc[df['Summary'] == a[0], 'content'].iloc[0]
    resultContent = a[0] + '. '+ a[1]

    textSplitter = RecursiveCharacterTextSplitter()
    text = textSplitter.split_text(resultContent)


    chroma_CSV_VectorIndex = Chroma.from_texts(text, GeminiEmbeddingModel)


    retriever = chroma_CSV_VectorIndex.as_retriever()
    Question_Answer_Chain = create_retrieval_chain(retriever, document_retrieval_chain)

    result = Question_Answer_Chain.invoke({"input": query})
    return result["answer"]


