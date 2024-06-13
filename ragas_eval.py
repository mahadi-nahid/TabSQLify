import os

os.environ["OPENAI_API_KEY"] = "" ## API Key 

# OPENAI_API_KEY = "" ## API KEY 


from datasets import load_dataset

from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)


data = load_dataset("json", data_files="outputs/fetaqa_fulltable_C_Ragas.jsonl")

print(data)


from ragas import evaluate
from datasets import Dataset

# from datasets import load_dataset
#
# fiqa_eval = load_dataset("explodinggradients/fiqa", "ragas_eval")
#
# print(fiqa_eval)


# from ragas import evaluate
# result = evaluate(
#     fiqa_eval["baseline"].select(range(3)), # selecting only 3
#     metrics=[
#         context_precision,
#         faithfulness,
#         answer_relevancy,
#         context_recall,
#     ],
# )

#
# result = evaluate(
#     data["train"].select(range(1000, 1050)), # selecting only 3
#     metrics=[
#         context_precision,
#         faithfulness,
#         answer_relevancy,
#         context_recall,
#     ],
# )
#
# print(result)


# prepare your huggingface dataset in the format
# Dataset({
#     features: ['question', 'contexts', 'answer', 'ground_truths'],
#     num_rows: 25
# })

# dataset: Dataset

# results = evaluate(data)
# {'ragas_score': 0.860, 'context_precision': 0.817,
# 'faithfulness': 0.892, 'answer_relevancy': 0.874}