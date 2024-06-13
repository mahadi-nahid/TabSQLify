import pandas as pd


import json
import pandas as pd
from sqlalchemy import create_engine
from pandasql import sqldf
import tqdm

from utils.preprocess import preprocess_columns

if __name__ == "__main__":
    path_wikiTQ = "../datasets/WikiTableQA/test_wikitqa.json"
    with open(path_wikiTQ) as f:
        wikitableqa = json.load(f)
    start = 20
    # end = len(wikitableqa)
    end = start + 1
    keys = list(wikitableqa.keys())[start:end]

    sql = """select * from T"""
    # ---------------------------------------------------------------
    error_keys = []

    for key in tqdm.tqdm(keys):
        entry = wikitableqa[key]
        question = entry['question']
        title = entry['title']
        table = entry['table']
        answer = entry['answer']
        table_id = entry['table_id']

        print('key: ', key, ' Table Id: ', 'title: ', table_id, title)
        print('Q: ', question)

        engine = create_engine('sqlite:///database.db')

        table_path = '../datasets/WikiTableQA/' + table_id
        df = pd.read_csv(table_path, encoding='utf-8')
        print(df.head())
        columns = preprocess_columns(df.columns)
        df.columns = columns
        print(df.columns)
        # df = df.assign(row_number=range(len(df)))
        print("Original DataFrame:")
        print(df)

        # Select 5 random rows and create a copy of them
        random_rows = df.sample(n=5).copy()
        # Modify the values in the selected rows
        rows = pd.DataFrame()
        i = len(df)
        print('len: ', i)
        for index, row in random_rows.iterrows():
            for column in df.columns:
                # Append '_mod' to the value and save it back to the DataFrame
                rows.at[i, column] = str(row[column]) + '_mod'
            i += 1

        print('random_rows:\n\n', rows)
        new_df = pd.concat([df, rows])

        # Append the modified rows to the original DataFrame
        # df = df.append(random_rows, ignore_index=True)

        new_df = new_df.assign(row_number=range(len(df)))
        print('new_df:\n\n', new_df)

        query = "select * from df"

        result = sqldf(query, locals())

        # result_list = result.values.tolist()
        # for row in result_list:
        #     for coll in row:
        #         print(coll)

        print('Results:\n--------------\n', result, type(result))


