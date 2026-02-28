import pandas as pd
from datasets import Dataset
data ={
    'question': [
        "Where did this canditate go to university?",
        "What is the name of the candidate?",
        "What is the candidates's experience with python?",
        "has this candidate worked on any AI projects?"
    ],
    'ground_truth':[
        "the candidate attended the APJ Abdul Kalam Technical University and studied B.tech in Applied electronics and instrumentation engineering.",
        "the candidate's name is Vaishnav AK.",
        "the candidate has 3 years of experience with Python.",
        "the candidate has worked on several AI projects including image classification and natural language processing."
    ],
    'contexts':[
        ["Education in B.tech in Applied electronics and instrumentation engineering from APJ Abdul Kalam Technical University,2019-23."],
        ["Name: Vaishnav AK."],
        ["Skills: Python (3 years of experience)"],
        ["projects: Image classification using CNN, Natural language processing"],

    ]

}
def prepare_dataset():
    dataset = Dataset.from_dict(data)
    print("Resume Test Dataset Created Successfully!")
    print(dataset)
    return dataset
if __name__ == "__main__":
    prepare_dataset()
    