# 🕵️‍♂️ Autonomous Analyst Agent

An AI Agent capable of analyzing local data (CSV) and searching the live web to answer complex questions. Built with Python, LangChain, and Groq (Llama 3).

## 🚀 Features
*   **Data Analysis:** Uses a Pandas Agent to read CSV files, calculate statistics, and generate Python visualizations (Matplotlib) on the fly.
*   **Web Search:** Integrates DuckDuckGo to fetch real-time information (Stock prices, News).
*   **Intelligent Routing:** Automatically decides whether to use the Data Tool or Search Tool based on user intent.
*   **Interactive UI:** Built with Streamlit for a chat-like experience.

## 🛠️ Tech Stack
*   **LLM:** Llama-3.3-70b (via Groq API)
*   **Orchestration:** LangChain & LangChain Experimental
*   **Frontend:** Streamlit
*   **Tools:** Pandas, DuckDuckGo Search (ddgs)

## ⚙️ Setup & Installation

1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/vaishnavak2001/Autonomous-Analyst-Agent.git
    cd Autonomous-Analyst-Agent
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables:**
    Create a `.env` file in the root directory and add your Groq API Key:
    ```
    GROQ_API_KEY=gsk_...
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

