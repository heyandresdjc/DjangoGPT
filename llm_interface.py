import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate


MODEL = "llama3.1"
EMBEDDINGS_MODEL = "nomic-embed-text"
CHROMA_COLLECTION_NAME = "local_andres"


def run_llm(question: str) -> dict:
    vector = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=OllamaEmbeddings(model=EMBEDDINGS_MODEL, show_progress=True)
    )

    # Input
    retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = Ollama(model=MODEL)

    prompt = """
        1. Use the following pieces of context to answer the question at the end.\n
        2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
        3. Keep the answer crisp and limited to 3,4 sentences.\n
        4. All response should come back in a HTML separated in 2 elements first explanation then code example \n 
    
        Context: {context}
        
        Question: {question}
        
        Helpful Answer:"""

    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt),
        callbacks=None,
        verbose=False
    )

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context",
        document_prompt=PromptTemplate(
            input_variables=["page_content", "source"],
            template="Context:\ncontent:{page_content}\nsource:{source}",
        ),
        callbacks=None
    )

    qa = RetrievalQA(
        combine_documents_chain=combine_documents_chain,
        verbose=False,
        retriever=retriever,
        return_source_documents=True
    )

    return qa(question)


def create_vector_interface(document_location: str):
    loader = PyPDFLoader(document_location)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    documents = text_splitter.split_documents(docs)

    # Instantiate the embedding model
    embedder = OllamaEmbeddings(model=EMBEDDINGS_MODEL, show_progress=True)

    # Create the vector store
    Chroma.from_documents(
        documents,
        embedder,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory="chroma_data"
    )


def add_document(document_location: str) -> bool:
    
    print(f"Processing {document_location}")

    loader = PyPDFLoader(document_location)
    docs = loader.load()
    embedder = OllamaEmbeddings(model=EMBEDDINGS_MODEL, show_progress=True)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
    documents = text_splitter.split_documents(docs)
    vector = Chroma(collection_name=CHROMA_COLLECTION_NAME, embedding_function=embedder)
    vector.add_documents(documents)
    return True
