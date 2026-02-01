import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Import the custom search tool logic
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

load_dotenv()

# --- CONFIGURATION ---
LLM_MODEL = "llama-3.3-70b-versatile"

def initialize_llm():
    return ChatGroq(model=LLM_MODEL, temperature=0)

# --- TOOLS ---

def search_web(query):
    """Deep search using DuckDuckGo."""
    print(f"DEBUG: Searching web for: {query}")
    try:
        with DDGS() as ddgs:
            # We use list() to consume the generator immediately
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}" for r in results])
            return "No results found."
    except Exception as e:
        return f"Search Error: {e}"

def analyze_data(query):
    """Analyzes the Titanic dataset using Pandas Agent."""
    print(f"DEBUG: Analyzing data for: {query}")
    
    # Check if data exists
    if not os.path.exists("data/titanic.csv"):
        return "Error: 'data/titanic.csv' not found.", None
    
    df = pd.read_csv("data/titanic.csv")
    llm = initialize_llm()
    
    # Create Agent
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True
    )
    
    # Clean old plot
    if os.path.exists("plot.png"):
        os.remove("plot.png")
        
    # Run Query
    enhanced_query = query + " If you plot a chart, save it as 'plot.png'."
    try:
        result = agent.invoke(enhanced_query)
        output_text = result['output']
    except Exception as e:
        output_text = f"Error running agent: {e}"
    
    # Check for image side-effect
    image_path = "plot.png" if os.path.exists("plot.png") else None
    
    return output_text, image_path

# --- ROUTER ---

def route_query(query):
    """Decides if the query is DATA or SEARCH."""
    llm = initialize_llm()
    
    router_prompt = PromptTemplate.from_template("""
    Classify the following question into 'DATA' or 'SEARCH'.
    
    1. 'DATA': Questions about the Titanic dataset, passengers, survival, ages, stats, or plotting charts.
    2. 'SEARCH': Questions about current events, stock prices, news, weather, or general knowledge.
    
    Question: {question}
    
    Return ONLY the word 'DATA' or 'SEARCH'.
    """)
    
    chain = router_prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"question": query})
        return response.strip()
    except Exception:
        return "SEARCH" # Fallback

# --- MAIN ENTRY POINT ---

def get_agent_response(user_input):
    """The Master Function called by the UI."""
    
    # 1. Route
    category = route_query(user_input)
    print(f"DEBUG: Routing decision -> {category}")
    
    # 2. Execute
    if category == "DATA":
        response_text, image_path = analyze_data(user_input)
        return response_text, image_path, "DATA"
    
    else: # SEARCH
        # Conversational Search
        llm = initialize_llm()
        search_results = search_web(user_input)
        
        summary_prompt = PromptTemplate.from_template("""
        Answer the user's question based on these search results.
        
        Question: {question}
        Search Results: {results}
        
        Answer:
        """)
        chain = summary_prompt | llm | StrOutputParser()
        response_text = chain.invoke({"question": user_input, "results": search_results})
        
        return response_text, None, "SEARCH"

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("\n--- TEST 1: SEARCH ---")
    print(get_agent_response("Who is the CEO of Tesla?")[0])
    
    print("\n--- TEST 2: DATA ---")
    print(get_agent_response("What is the average age of passengers?")[0])