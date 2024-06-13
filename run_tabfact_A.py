import csv
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from utils.preprocess import *
from utils.normalizer import *
from utils.prompt_tabfact import *

def tabsqlify_tabfact(T, title, tab_col, statement, three_row, selection='rc'):
    # selection = ['col', 'row', 'rc', 'sql']
    prompt = gen_table_decom_prompt(title, tab_col, statement, three_row, selection=selection)
    # print(prompt)
    sql = get_sql_3(prompt)

    response = ""
    # output_ans = ""
    linear_table = ""

    print('\nM1: ', sql, '\n')

    result = pd.DataFrame()
    try:
        result = sqldf(sql, locals())
    except:
        print('error --> id: ', i, id)
        # empty_error_ids.append(i)
        # continue
    if not result.empty:
        linear_table = table_linearization(result, style='pipe')

    else:
        print('empty. id --> ', i, id)
        empty_error_ids.append(i)
        prompt = gen_table_decom_prompt(title, tab_col, statement, three_row, selection='col')
        sql = get_sql_3(prompt)
        # sql = sql.split('where')[0]
        print('col sql: ', sql)
        try:
            result = sqldf(sql, locals())
        except:
            print('col selection - empty/error')
        if not result.empty and result is not None:
            linear_table = table_linearization(result, style='pipe')
        else:
            sql = "select * from T"
            result = sqldf(sql, locals())
            linear_table = table_linearization(result, style='pipe')

    return sql, result, linear_table


if __name__ == "__main__":

    path = 'datasets/tabfact_small_test.jsonl'

    start = 0
    end = start + 100
    table_ids = list(range(start, end))

    correct = 0
    wrong = 0
    t_samples = 0
    empty_error_ids = []

    # tabsqlify = True
    tabsqlify = False

    with open(path, encoding='utf-8') as f1:
        # --------------------------------------------------------------
        fw = open(f'outputs/tf_0_10_fulltable.jsonl', 'a')

        # ---------------------------------------------------------------
        f = open('outputs/tf_0_10_fulltable.csv', 'a')
        writer = csv.writer(f)
        header = ['id', 'statement', 'response', 'label', 'prediction', 'sql',  'r_num_cell', 't_num_cell', 'context']
        writer.writerow(header)
        # ---------------------------------------------------------------

        for i, l in enumerate(f1):
            if i in table_ids:
                dic = json.loads(l)
                id = dic['table_id']
                title = dic['table_caption']
                table = dic['table_text']
                statement = dic['statement']
                label = dic['label']
                print('\n\nid: ', id, ' S: ', statement, ' ans: ', label)

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

                # ----------------------------------------------------------------------------------------------
                sql = ""
                # ----------------------------------------------------------------------------------------------
                if tabsqlify == True:
                    sql_3 = """select * from T limit 3"""
                    three_row = sqldf(sql_3, locals())
                    three_row = table_linearization(three_row, style='pipe')
                    # print('\nThree example rows: \n', str(three_row))
                    sql, result, linear_table = tabsqlify_tabfact(T, title, tab_col, statement, three_row, selection='rc')
                    print('sql: ', sql, '\nlinear_table:\n', linear_table)
                    prompt_ans = generate_sql_answer_prompt(title, sql, linear_table, statement)
                    # print(prompt_ans)
                    response = get_answer(prompt_ans)

                    t_num_cell = T.size
                    r_num_cell = result.size

                    print('R num_cell: ', r_num_cell, 'T num_cell: ', t_num_cell)

                else:
                    linear_table = table_linearization(T, style='pipe')
                    prompt_ans = gen_full_table_prompt(title, linear_table, statement)
                    response = get_answer(prompt_ans)

                    sql = ""
                    t_num_cell = T.size
                    r_num_cell = T.size


                if 'not possible to verify' in response:
                    predict = 2
                elif 'cannot be verified' in response:
                    predict = 2
                elif 'no information' in response:
                    predict = 2
                elif 'cannot be determined' in response:
                    predict = 2
                elif 'true' in response:
                    predict = 1
                elif 'false' in response:
                    predict = 0
                elif 'support' in response:
                    predict = 1
                else:
                    predict = 3

                if predict == label:
                    correct += 1
                else:
                    wrong += 1

                t_samples += 1

                print('\nResponse: ', response, '\nPrediction: ', predict, 'Gold: ', label)

                print('Correcet: ', correct, 'wrong: ', wrong, 'total: ', t_samples, "Accuracy: ", correct / (t_samples + 0.0001))

            # ---------------------------------------------------------------------------------------------------------
                tmp = {'key': id, 'statement': statement, 'response': response, 'label': label}
                fw.write(json.dumps(tmp) + '\n')
            #
                data = [id, statement, response, label, predict, sql, r_num_cell, t_num_cell, linear_table]
                writer.writerow(data)

            # ---------------------------------------------------------------------------------------------------------

    f.close()
    fw.close()
    print('Final --> Correcet: ', correct, 'wrong: ', wrong, 'total: ', t_samples, "Accuracy: ", correct / (t_samples + 0.0001))
    print('empty_error_ids: ', empty_error_ids)
# --------------------------------------------------------------------------