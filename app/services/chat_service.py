import os
from dotenv import load_dotenv
from collections import deque

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# --- Load environment variables ---
load_dotenv(override=True)

# --- Load Mistral LLM ---
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("MISTRAL_API_KEY"),
)

# --- Vectorstore setup ---
faiss_index_path = "vectorstore/faiss_index"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- MySQL Database Setup ---
db = SQLDatabase.from_uri(os.getenv("MYSQL_URI"))
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

sql_agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# --- Memory Buffer for last k=5 interactions ---
conversation_history = deque(maxlen=5)


# --- Hybrid Chat Function with Memory ---
def chat(query: str):
    """
    Process a user query by integrating vectorstore retrieval, SQL database querying,
    and conversation memory to generate a context-aware AI response.

    Args:
        query (str): The user input query.

    Returns:
        dict: A dictionary containing the AI-generated response under the key 'ai_response'.
    """

    # --- 1. Vectorstore Retrieval ---
    # Load FAISS vectorstore index and retrieve top 3 relevant documents for the query.
    faiss_store = FAISS.load_local(
        faiss_index_path, embeddings, allow_dangerous_deserialization=True
    )
    retriever = faiss_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    rag_context = "\n\n".join([doc.page_content for doc in docs])

    # --- 2. SQL Query Execution ---
    # Execute the query on the connected MySQL database using the SQL agent.
    try:
        sql_response = sql_agent.run(query)
    except Exception as e:
        sql_response = f"Error querying database: {str(e)}"

    # --- 3. Construct Memory Context ---
    # Aggregate last 5 conversation turns to maintain context.
    memory_context = ""
    for human_msg, ai_msg in conversation_history:
        memory_context += f"Human: {human_msg}\nAssistant: {ai_msg}\n"

    # --- 4. Prompt Construction ---
    # Build the prompt template incorporating conversation history, retrieved documents,
    # and SQL query results to guide the LLM's response.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant with access to business documents and a MySQL database.

Conversation history:
{memory_context}

Context from documents:
{rag_context}

Information from MySQL database:
{sql_response}

Answer the user question using the information above. If any required information is missing, say so politely.""",
            ),
            ("human", "{query}"),
        ]
    )

    # --- 5. LLM Inference ---
    # Combine the prompt with the LLM and invoke it with all contextual inputs.
    chain = prompt | llm
    final_response = chain.invoke(
        {
            "query": query,
            "sql_response": sql_response,
            "rag_context": rag_context,
            "memory_context": memory_context,
        }
    )

    # --- 6. Update Memory ---
    # Append the current user query and AI response to the conversation history.
    conversation_history.append((query, final_response.content))

    return {"ai_response": final_response.content}
