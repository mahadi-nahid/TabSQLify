import json
import csv
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from utils.preprocess import *
from utils.normalizer import *
from utils.prompt_fetaqa import *


def merge_json_files(file_a, file_b, output_file):
    # Load data from A.jsonl
    with open(file_a, 'r', encoding='utf-8') as file:
        data_a = [json.loads(line) for line in file]

    # Load data from B.json
    with open(file_b, 'r', encoding='utf-8') as file:
        data_b = [json.loads(line) for line in file]

    # Create a dictionary to map 'fetaqa_id' to its corresponding entry in A.jsonl
    a_mapping = {entry['feta_id']: entry for entry in data_a}

    print('data_a: ', data_a[0], '\ndata_b: ', data_b[0])
    # Merge data based on common 'fetaqa_id' and 'key' values
    fw2 = open(output_file, 'a')

    merged_data = []
    for entry_b in data_b:

        for entry_a in data_a:
            # key = entry_b['key']
            # feta_id = entry_a['feta_id']
            # print(key, type(key), feta_id, type(feta_id))

            if int(entry_b['key']) == entry_a['feta_id']:

                id = entry_a['feta_id']
                title = entry_a['table_page_title']
                subtitle = entry_a['table_section_title']
                table = entry_a['table_array']
                question = entry_b['question']
                answer = entry_b['answer']
                answer = answer.lower()
                response = entry_b['response']

                print('\n\nid: ', id, 'key: ', entry_b['key'], 'Q: ', question, '\nresponse: ', response, '\nans: ', answer)

                T = dict2df(table)
                T = T.assign(row_number=range(len(T)))
                row_number = T.pop('row_number')
                T.insert(0, 'row_number', row_number)
                col = T.columns
                linear_table = table_linearization(T, style='pipe')

                # -------------------------------------------------------------------------------------
                context = []
                context.append(title)
                context.append(subtitle)
                context.append(linear_table)

                ground_truth = []
                ground_truth.append(answer)

                tmp = {'question': question, 'contexts': context, 'answer': response, 'ground_truths': ground_truth}
                fw2.write(json.dumps(tmp) + '\n')

        # if feta_id in a_mapping:
        #     entry_a = a_mapping['feta_id']
        #     merged_entry = {**entry_a, **entry_b}
        #     merged_data.append(merged_entry)

    fw2.close()
    # # Write the merged data to the output file
    # with open(output_file, 'w', encoding='utf-8') as output:
    #     json.dump(merged_data, output, ensure_ascii=False, indent=2)


def write_ragas():
    start = 0
    end = start + 5

    table_ids = list(range(start, end))

    empty_error_ids = []

    with open('datasets/fetaQA-v1_test.jsonl', encoding='utf-8') as f1:
        # --------------------------------------------------------------
        # fw = open(f'outputs/fetaqa_col_C.jsonl', 'a')
        fw2 = open(f'outputs/fetaqa_fulltable_C_Ragas.jsonl', 'a')
        # tmp = {'demonstration': p_direct_sql_wikiTQ}
        # fw.write(json.dumps(tmp) + '\n')

        # ---------------------------------------------------------------
        # f = open('outputs/fetaqa_col_C.csv', 'a')
        # writer = csv.writer(f)
        # header = ['id', 'question', 'response', 'answer', 'sql',  'r_num_cell', 't_num_cell', 'linear_table']
        # writer.writerow(header)
        # ---------------------------------------------------------------
        sample = 0
        for i, l in enumerate(f1):
            if i in table_ids:
                dic = json.loads(l)
                id = dic['feta_id']
                title = dic['table_page_title']
                subtitle = dic['table_section_title']
                table = dic['table_array']
                question = dic['question']
                answer = dic['answer']
                answer = answer.lower()
                response = dic['response']

                print('\n\nid: ', id, ' Q: ', question, ' ans: ', answer)

                T = dict2df(table)
                T = T.assign(row_number=range(len(T)))
                row_number = T.pop('row_number')
                T.insert(0, 'row_number', row_number)
                col = T.columns

                # -------------------------------------------------------------------------------------
                context = []
                context.append(title)
                context.append(subtitle)

                ground_truth = []
                ground_truth.append(answer)

                # # print('Table Coll: ', col)
                # tab_col = ""
                # for c in col:
                #     tab_col += c + ", "
                # tab_col = tab_col.strip().strip(',')
                # print('Table Column: ', tab_col)

                # --------------------------------------------------------------------------------------

                T = convert_df_type(T)

                linear_table = table_linearization(T, style='pipe')

                context.append(linear_table)
                print('q: ', question, '\ncontext: ', context, '\nans: ', response, '\nground_truth: ', ground_truth)

                # ---------------------------------------------------------------------------------------------------------
                # tmp = {'key': id, 'question': question, 'response': response, 'answer': answer, 'table': linear_table}
                # fw.write(json.dumps(tmp) + '\n')
                #
                # data = [id, question, response, answer, sql, r_num_cell, t_num_cell, linear_table]
                # writer.writerow(data)

                tmp = {'question': question, 'contexts': context, 'answer': response, 'ground_truths': ground_truth}
                # fw2.write(json.dumps(tmp) + '\n')
                # ---------------------------------------------------------------------------------------------------------

    # f.close()
    # fw.close()
    # fw2.close()



# Example usage:
merge_json_files('fetaQA-v1_test.jsonl', 'FeTaQA_Full_1.json', 'outputs/fetaqa_fulltable_C_Ragas.jsonl')



