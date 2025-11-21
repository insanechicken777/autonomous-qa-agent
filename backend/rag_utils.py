import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_PATH = "./vector_db"

def build_knowledge_base(upload_dir: str):
    print(f"Processing files from: {upload_dir}")
    loader = DirectoryLoader(upload_dir, glob="**/*", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        return {"status": "error", "message": "No documents found."}

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        persist_directory=DB_PATH
    )
    
    return {"status": "success", "chunks_processed": len(chunks)}

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found")
    
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=api_key
    )

def generate_test_cases(query: str):
    """
    Updated to use the modern 'create_retrieval_chain'
    """
    # 1. Load DB
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embedding_model)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 2. Define Prompt
    system_prompt = (
        "You are a QA Automation Lead. Use the context provided below to generate comprehensive test cases. "
        "Output strictly JSON format with keys: test_id, description, expected_result, grounded_in. "
        "Do not output Markdown code blocks.\n\n"
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 3. Create the Chain (The Modern Way)
    llm = get_llm()
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 4. Run it
    response = rag_chain.invoke({"input": query})
    
    # The answer is in the 'answer' key
    return response["answer"]

def generate_selenium_script(test_case: str, html_content: str):
    llm = get_llm()
    
    prompt_text = f"""
    You are a Senior SDET. Write a Python Selenium script for the SPECIFIC test case provided below.
    
    --- INPUT DATA ---
    Test Case JSON: {test_case}
    Target HTML: {html_content}
    
    --- FILE LOCATION ---
    The HTML file is located at: "assets/checkout.html" (Relative to the script).
    
    --- SCOPE RESTRICTION ---
    1. Generate code ONLY for the specific test case.
    
    --- LOGIC FLOW ---
    1. SETUP:
       - Init Driver.
       - Define path: `file_path = os.path.abspath("assets/checkout.html")`
       - Open file: `driver.get(f"file:///{{file_path}}")`
       
       # --- SMART CART LOGIC ---
       - IF the test description contains "empty", DO NOT add items.
       - ELSE IF testing 'SAVE15' or generic discount, add items (`btn-add-headphones`) to ensure total > 0.
       - IF testing 'FREESHIP', select 'express' shipping.
       
       - Wait 1s for JS updates.
    
    2. CAPTURE & ACTION:
       - Capture `price_before` (float).
       - Perform Action (Input Code -> Click Apply).
       - Wait 1s (or WebDriverWait if text expects to change).
       - Capture `price_after` (float).
    
    3. ASSERTION:
       - IF "empty" or "invalid": `expected = price_before` (No change).
       - IF "SAVE15" and valid: `expected = price_before * 0.85`.
       - IF "FREESHIP": `expected = price_before - 10`.
       - Assert `abs(price_after - expected) < 0.01`.
    
    4. FINISH:
       - time.sleep(10)
       - driver.quit()
       
    Return ONLY raw Python code.
    """
    
    response = llm.invoke(prompt_text)
    return response.content