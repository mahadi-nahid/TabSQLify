import csv
from pandasql import sqldf
from sqlalchemy import create_engine
import pandas as pd
from utils.preprocess import *
from utils.prompt_wtq import *
from utils.normalizer import *

start = 1283
end = start + 1

table_ids = list(range(start, end))
# 70-80
# large_table_ids = [30, 44, 141, 158, 208, 237, 263, 279, 348, 367, 395, 401, 441, 444, 514, 546, 553, 573, 575, 642, 659, 690, 699, 718, 766, 904, 919, 936, 973, 999, 1004, 1008, 1014, 1041, 1073, 1084, 1109, 1140, 1166, 1185, 1259, 1330, 1365, 1382, 1406, 1430, 1453, 1596, 1617, 1624, 1627, 1671, 1707, 1844, 1873, 1877, 1895, 1899, 1918, 1945, 1955, 1969, 2019, 2047, 2100, 2160, 2191, 2212, 2219, 2235, 2243, 2292, 2293, 2323, 2355, 2359, 2439, 2443, 2504, 2552, 2565, 2630, 2633, 2650, 2673, 2696, 2729, 2797, 2816, 2819, 2900, 2906, 2908, 3040, 3092, 3139, 3158, 3203, 3228, 3253, 3290, 3294, 3419, 3434, 3469, 3487, 3573, 3624, 3662, 3663, 3679, 3693, 3706, 3709, 3711, 3732, 3750, 3941, 3990, 4004, 4007, 4068, 4085, 4188, 4194, 4196, 4222, 4299]
# print(len(large_table_ids))
# large_table_ids = large_table_ids[126:129]

correct = 0
t_samples = 0
empty_error_ids = []

with open('../datasets/wtq_test3.jsonl', encoding='utf-8') as f1:
    # --------------------------------------------------------------
    # fw = open(f'wktq_col_nov5_A.jsonl', 'a')
    # tmp = {'demonstration': p_direct_sql_wikiTQ}
    # fw.write(json.dumps(tmp) + '\n')

    # ---------------------------------------------------------------
    # f = open('wktq_col_nov5_A.csv', 'a')
    # writer = csv.writer(f)
    # header = ['id', 'question', 'answer', 'prediction', 'sql',  'r_num_cell', 't_num_cell']
    # writer.writerow(header)
    # ---------------------------------------------------------------

    for i, l in enumerate(f1):

        if i in table_ids:
            dic = json.loads(l)
            ids = dic['ids']
            title = dic['title']
            table = dic['table_text']
            question = dic['statement']
            answer = dic['answer']
            answer = ','.join(answer)
            answer = answer.lower()
            print('\n\nid: ', ids, ' Q: ', question, ' ans: ', answer)

            # headers = table[0]
            # print(headers)
            #
            # table = [headers] + table

            T = dict2df(table)
            T = T.assign(row_number=range(len(T)))
            row_number = T.pop('row_number')
            T.insert(0, 'row_number', row_number)
            col = T.columns

            # print('Table Coll: ', col)
            tab_col = ""
            for c in col:
                tab_col += c + ", "
            tab_col = tab_col.strip().strip(',')
            print('Table Column: ', tab_col)


            # --------------------------------------------------------------------------------------
            engine = create_engine('sqlite:///database.db')
            # T = prepare_df_for_neuraldb_from_table(table)

            T = convert_df_type(T)

            print('W:\n\n', T)
            #
            # df = T
            # df.to_sql(name='w', con=engine, if_exists='replace')
            #
            # with engine.connect() as conn:
            #     rs = conn.execute(text("SELECT * FROM w")).fetchall()

            # print('df to db')
            # for r in rs:
            #     print(r)
            # ----------------------------------------------------------------------------------------------
            sql_3 = """select * from T"""
            # sql_3 = """SELECT year FROM T WHERE back_of_shirt_sponsor = 'psu technology group'"""
            three_row = sqldf(sql_3, locals())
            three_row = table_linearization(three_row, style='pipe')
            print('\nThree example rows: \n', str(three_row))
