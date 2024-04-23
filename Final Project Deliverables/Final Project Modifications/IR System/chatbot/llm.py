
#******************************Libraries**********************************
import pandas as pd
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
# from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from rank_bm25 import BM25Okapi
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

#******************************** LLM MODEL ******************************************
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

#******************************** LLM Embeddings *****************************
GeminiEmbeddingModel = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key="AIzaSyBSaMUOmN4usfGXD9PT7OmDcCFCa9WvBMc")

#******************************** Preparing data ********************************
df = pd.read_csv('cricket_football_preprocessed.csv')
headingsList = df["content"].tolist()
tokenized_corpus = [doc.split(" ") for doc in headingsList]

bm25 = BM25Okapi(tokenized_corpus)
# Explain about the following Topic in depth using the provided context and your knowledge
#****************************** Prompt creation **********************************
prompt = ChatPromptTemplate.from_template(
"""
Context:
{context}

Question:
{input}
""")


#**************************** Chaining Prompt and LLM ******************************
document_retrieval_chain = create_stuff_documents_chain(Gemini_pro_llm, prompt)



def ask_Query(query):
    tokenized_query = query.split(" ")
    # doc_scores = bm25.get_scores(tokenized_query)

    a = bm25.get_top_n(tokenized_query, headingsList, n=2)
    # a[0] = "Sport as a Symbol of National Power" # hardcoded
    # resultContent = df.loc[df['Summary'] == a[0], 'content'].iloc[0]
    doc = ""
    for i in range(2):
        doc = doc + a[i] + '. '
    resultContent = doc

    textSplitter = RecursiveCharacterTextSplitter()
    text = textSplitter.split_text(resultContent)


    chroma_CSV_VectorIndex = Chroma.from_texts(text, GeminiEmbeddingModel)


    retriever = chroma_CSV_VectorIndex.as_retriever()
    Question_Answer_Chain = create_retrieval_chain(retriever, document_retrieval_chain)

    result = Question_Answer_Chain.invoke({"input": query})

    return result["answer"]


