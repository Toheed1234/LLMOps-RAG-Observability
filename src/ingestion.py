import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

def ingest_documents(data_dir="data", persist_dir="data/chroma_db"):
    """
    Reads all text and pdf files in the data_dir, chunks them, and stores them in ChromaDB.
    """
    documents = []
    
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return

    # Loop through the files in /data/
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if filename.endswith(".txt"):
            print(f"Loading {filename}...")
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
        elif filename.endswith(".pdf"):
            print(f"Loading {filename}...")
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
            
    if not documents:
        print(f"No documents found in {data_dir}. Please add some .txt or .pdf files.")
        return

    # Split documents into small readable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    print(f"Split documents into {len(docs)} chunks.")

    # Generate Embeddings & Store in Local Vector DB
    # We use HuggingFace embeddings which run on the CPU locally(DUE TO USING AMD GPU AND HAVING ISSUES WITH WINDOWS COMPATIBILITY)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("Vectorizing and persisting to ChromaDB...")
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_dir)
    # Note: Depending on the Chroma version, persist() is sometimes called automatically
    vectorstore.persist()
    print(f"Successfully ingested and persisted database to {persist_dir}")

if __name__ == "__main__":
    ingest_documents()
