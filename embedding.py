from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 


load_dotenv()


api_key = os.environ['Api_key']
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=api_key,
    temperature=0.7
)

def get_vectorstore(text_chunks):
    """
    Create a FAISS vectorstore from a list of text chunks using 
    a token-free SentenceTransformer embedding model.
    
    Args:
        text_chunks (list[str]): List of text strings to embed.

    Returns:
        FAISS vectorstore
    """
    
    # Use a token-free sentence transformer model
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Convert text chunks to LangChain Documents
    docs = [Document(page_content=chunk) for chunk in text_chunks]
    
    # Build FAISS vectorstore
    vectordb = FAISS.from_documents(documents=docs, embedding=embeddings_model)
    
    return vectordb


def get_conversation_chain(vectorstore):
    # memory keeps chat history automatically
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # singular key in memory
        return_messages=True        # must be True, not return_message
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=False  # optional
    )

    return conversation_chain

