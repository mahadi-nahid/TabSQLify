import csv
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from utils.preprocess import *
from utils.normalizer import *
from utils.prompt_fetaqa import *

def tabsqlify_fetaqa(T, title, tab_col, question, three_row, selection='rc'):
    # selection = ['col', 'row', 'rc', 'sql']
    prompt = gen_table_decom_prompt(title, tab_col, question, three_row, selection=selection)
    sql = get_sql_3(prompt)

    print('\nM1: ', sql, '\n')

    response = ""
    # output_ans = ""
    linear_table = ""

    result = pd.DataFrame()
    try:
        result = sqldf(sql, locals())
    except:
        print('error --> id: ', i, id)

    if not result.empty and result is not None:
        linear_table = table_linearization(result, style='pipe')
    else:
        print('empty. id --> ', i, id)
        empty_error_ids.append(i)
        prompt = gen_table_decom_prompt(title, tab_col, question, three_row, selection='col')
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

    path = 'fqa_cut_more_than_50_percent.jsonl'

    start = 0
    end = start + 210

    table_ids = list(range(start, end))

    empty_error_ids = []

    tabsqlify = True
    # tabsqlify = False

    with open(path, encoding='utf-8') as f1:
        # --------------------------------------------------------------
        # fw = open(f'outputs/fqa_0_to_10_rc.jsonl', 'a')
        # fw2 = open(f'outputs/fqa_0_to_10_rc_ragas.jsonl', 'a')
        # tmp = {'demonstration': p_direct_sql_wikiTQ}
        # fw.write(json.dumps(tmp) + '\n')

        # ---------------------------------------------------------------
        # f = open('outputs/fqa_0_to_10_rc.csv', 'a')
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

                if tabsqlify == True:
                    # ----------------------------------------------------------------------------------------------
                    sql_3 = """select * from T limit 3"""
                    three_row = sqldf(sql_3, locals())
                    three_row = table_linearization(three_row, style='pipe')
                    # print('\nThree example rows: \n', str(three_row))
                    sql, result, linear_table = tabsqlify_fetaqa(T, title, tab_col, question, three_row, selection='rc')

                    prompt_ans = generate_sql_answer_prompt(title, sql, linear_table, question)
                    # print(prompt_ans)
                    response = get_answer(prompt_ans)
                    response = response.lower().strip()

                    t_num_cell = T.size
                    r_num_cell = result.size
                    print('R num_cell: ', r_num_cell, 'T num_cell: ', t_num_cell)

                    # ----------------------------------------------------------------------------------------------

                else:
                    linear_table = table_linearization(T, style='pipe')
                    prompt_ans = get_full_table_prompt(title, linear_table, question)
                    # print(prompt_ans)
                    response = get_answer(prompt_ans)
                    response = response.lower().strip()
                    t_num_cell = T.size
                    r_num_cell = T.size
                    sql = ""

                print('\nAnswer gen output: ', response, '\nGold: ', answer)
                    # continue

                sample += 1
                print('sample# ', sample)

                context.append(linear_table)
                # print('q: ', question, 'context: ', context, 'ans: ', answer, 'ground_truth: ', ground_truth)

                # ---------------------------------------------------------------------------------------------------------
                # tmp = {'key': id, 'question': question, 'response': response, 'answer': answer, 'table': linear_table}
                # fw.write(json.dumps(tmp) + '\n')
                # # #
                # data = [id, question, response, answer, sql, r_num_cell, t_num_cell, linear_table]
                # writer.writerow(data)
                # #
                # tmp = {'question': question, 'contexts': context, 'answer': response, 'ground_truths': ground_truth}
                # fw2.write(json.dumps(tmp) + '\n')
                # ---------------------------------------------------------------------------------------------------------

    # f.close()
    # fw.close()
    # fw2.close()
    print('empty_error_ids: ', empty_error_ids)
# ---------------------------------------------------------------------------------------