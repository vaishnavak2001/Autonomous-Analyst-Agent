import os 
import pandas as pd
from datasets import Dataset
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.run_config import RunConfig
from dotenv import load_dotenv
from evaluation_setup import prepare_dataset

load_dotenv()
#1 setup llm as a judge(llama 3)
print("Setting up the LLM judge...")
groq_llm = ChatGroq(model="llama-3.1-8b-instant",temperature=0)
ragas_llm= LangchainLLMWrapper(groq_llm)
#2 setup embeddings
print("Setting up the embeddings...")
embeddings= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#3 rag simulation
print("Running RAG simulation...")
dataset = prepare_dataset()
def generate_mock_answer(row):
    return {"answer":row["ground_truth"]+"this is confirmed by the resume."}
dataset =dataset.map(generate_mock_answer)
print("starting ragas evaluation...")
metrics= [
    faithfulness,
    context_precision
]
run_config = RunConfig(max_workers=1,timeout=120)
try:
    results=evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=ragas_llm,
        embeddings=embeddings,
        run_config=run_config
    )
    print("\n Final report card")
    df=results.to_pandas()
    cols_to_show = ['question', 'faithfulness', 'context_precision']
    existing_cols_to_show=[c for c in cols_to_show if c in df.columns]

    print(df[existing_cols_to_show])
    df.to_csv("rag_evaluation_report.csv",index=False)
    print("\n Report saved to 'rag_evaluation_report.csv'")
except Exception as e:
    print(f"An error occurred during evaluation: {e}")
