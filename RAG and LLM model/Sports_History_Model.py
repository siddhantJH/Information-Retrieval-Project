# %%
! pip install -q --upgrade google-generativeai langchain-google-genai chromadb pypdf

# %%
! pip install langchain

# %%
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
# from langchain.chains import RetrievalQA
from langchain import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

# %%
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

# %%
Gemini_pro_llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                        google_api_key="<API-KEY>",
                                        temperature=1.0,
                                        convert_system_message_to_human=True,
                                        safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    })

# %%
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# %%
GeminiEmbeddingModel = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key="<API-KEY>")

# %%
# For PDF FILES
pdfLoader = PyPDFLoader("/content/2020- July-M.Tech.( CSE)-Regulations_Final.pdf")
pdf_pages = pdfLoader.load_and_split()

# %%
print(pdf_pages[1].page_content)

# %%
len(pdf_pages)

# %%
textSplitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap = 1000)


# %%
context = "\n\n".join(str(page.page_content) for page in pdf_pages)
text = textSplitter.split_text(context)

# %%
chroma_PDF_VectorIndex = Chroma.from_texts(text, GeminiEmbeddingModel).as_retriever(search_kwargs={"k":5})

# %%
QA_PDF_chain = RetrievalQA.from_chain_type(
    Gemini_pro_llm,
    retriever=chroma_PDF_VectorIndex,
    return_source_documents=True

)

# %%
! pip install beautifulsoup4

# %%
from langchain_community.document_loaders import WebBaseLoader
web_loader = WebBaseLoader(["https://en.wikipedia.org/wiki/Sport_in_India",
                            "https://www.indianetzone.com/28/memorable_events_indian_cricket.htm",])
documents = web_loader.load()

# %%
# Trying Recursive loader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

# %%
from bs4 import BeautifulSoup as Soup

url = "https://en.wikipedia.org/wiki/Sport_in_India"
recurrsive_loader = RecursiveUrlLoader(
    url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text
)
documents = recurrsive_loader.load()

# %%
text_splitter = RecursiveCharacterTextSplitter()
splitted_documents = text_splitter.split_documents(documents)
vector_index = Chroma.from_documents(splitted_documents, GeminiEmbeddingModel)

# %%
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_retrieval_chain = create_stuff_documents_chain(Gemini_pro_llm, prompt)

# %%
from langchain.chains import create_retrieval_chain

retriever = vector_index.as_retriever()
Question_Answer_Chain = create_retrieval_chain(retriever, document_retrieval_chain)

# %%
response = Question_Answer_Chain.invoke({"input": "who is the sachin tendulkar ?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...

# %%
import gradio as gr
# "What are the Requirements for M.tech Specialization. ?"
def ask_Query(Query):
    question = Query
    result = Question_Answer_Chain.invoke({"input": question})
    return result["answer"]

# %%
!pip install gradio

# %%
UI_Interface = gr.Interface(
    fn=ask_Query,
    inputs=gr.Textbox(lines=2, placeholder="Ask Query Here"),
    outputs="text",
)


# %%
UI_Interface.launch()


