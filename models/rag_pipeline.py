from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def load_and_process_pdfs(pdf_files):
    documents = []

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore



#8️⃣ Quick RAG Test (Confidence Booster)

def query_rag(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])
