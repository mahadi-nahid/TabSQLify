import csv
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from utils.preprocess import *
from utils.normalizer import *
from utils.prompt_wtq import *


def tabsqlify_wtq(T, title, tab_col, question, three_row, selection='rc'):
    # ----------------------------------------------------------------------------------------------
    # selection = ['col', 'row', 'rc', 'sql']
    prompt = gen_table_decom_prompt(title, tab_col, question, three_row, selection=selection)
    print(prompt)
    sql = get_sql_3(prompt)
    # sql = sql.split('where')[0]
    print('\nM1: ', sql, '\n')

    response = ""
    output_ans = ""
    linear_table = ""

    result = pd.DataFrame()
    try:
        result = sqldf(sql, locals())
    except:
        # print('error --> id: ', i, ids)
        # empty_error_ids.append(i)
        output_ans = "error"
        # continue

    if result.shape == (1, 1):
        result_list = result.values.tolist()
        # print('M1 - Result List: ', result_list, type(result_list))

        output_ans = ""
        for row in result_list:
            for coll in row:
                output_ans += str(coll) + " "
                # print(coll)
        response = "direct ans"
        output_ans = output_ans.lower()
        print('Direct ans: ', output_ans, 'Gold: ', answer)
        # continue
    elif not result.empty:
        # result_list = [result.columns.values.tolist()] + result.values.tolist()
        # print('M1 - Result List: ', result_list, type(result_list))

        linear_table = table_linearization(result, style='pipe')
        # print('M1 - Linear Table: \n', linear_table)

        prompt_ans = generate_sql_answer_prompt(title, sql, linear_table, question)
        print('promt_ans:\n', prompt_ans)
        response = get_answer(prompt_ans)
        print('response: ', response)
        try:
            output_ans = response.split("Answer:")[1]
            # print('Output answer: ', output_ans)
        except:
            print("Error: Answer generation.")
            output_ans = "" + response
        match = re.search(r'(The|the) answer is ([^\.]+)\.$', output_ans)
        if match:
            output_ans = match.group(2).strip('"')
        print('\nAnswer gen output: ', output_ans, 'Gold: ', answer)

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

        prompt_ans = generate_sql_answer_prompt(title, sql, linear_table, question)
        print('promt_ans:\n', prompt_ans)
        response = get_answer(prompt_ans)
        print('response: ', response)
        try:
            output_ans = response.split("Answer:")[1]
            # print('Output answer: ', output_ans)
        except:
            print("Error: Answer generation.")
            output_ans = "" + response
        match = re.search(r'(The|the) answer is ([^\.]+)\.$', output_ans)
        if match:
            output_ans = match.group(2).strip('"')
        print('\nAnswer gen output: ', output_ans, 'Gold: ', answer)


    return sql, result, response, output_ans, linear_table


if __name__ == "__main__":

    # path = 'wtq_cut_more_than_50_percent.jsonl'
    # path = 'wtq_cut_25_to_50_percent.jsonl'
    # path = 'wtq_cut_10_to_25_percent.jsonl'
    # path = 'wtq_cut_0_to_10_percent.jsonl'
    path = 'datasets/wtq_test3.jsonl'

    start = 507
    end = start + 1

    table_ids = list(range(start, end))
    # 70-80
    # large_table_ids = [30, 44, 141, 158, 208, 237, 263, 279, 348, 367, 395, 401, 441, 444, 514, 546, 553, 573, 575, 642, 659, 690, 699, 718, 766, 904, 919, 936, 973, 999, 1004, 1008, 1014, 1041, 1073, 1084, 1109, 1140, 1166, 1185, 1259, 1330, 1365, 1382, 1406, 1430, 1453, 1596, 1617, 1624, 1627, 1671, 1707, 1844, 1873, 1877, 1895, 1899, 1918, 1945, 1955, 1969, 2019, 2047, 2100, 2160, 2191, 2212, 2219, 2235, 2243, 2292, 2293, 2323, 2355, 2359, 2439, 2443, 2504, 2552, 2565, 2630, 2633, 2650, 2673, 2696, 2729, 2797, 2816, 2819, 2900, 2906, 2908, 3040, 3092, 3139, 3158, 3203, 3228, 3253, 3290, 3294, 3419, 3434, 3469, 3487, 3573, 3624, 3662, 3663, 3679, 3693, 3706, 3709, 3711, 3732, 3750, 3941, 3990, 4004, 4007, 4068, 4085, 4188, 4194, 4196, 4222, 4299]
    # print(len(large_table_ids))
    # large_table_ids = large_table_ids[126:129]

    correct = 0
    t_samples = 0
    empty_error_ids = []

    tabsqlify = True
    # tabsqlify = False

    with open(path, encoding='utf-8') as f1:
        # --------------------------------------------------------------
        # fw = open(f'outputs/wtq_0_to_10_fulltable.jsonl', 'a')
        # fw.write(json.dumps(tmp) + '\n')
        # ---------------------------------------------------------------
        # f = open('outputs/wtq_0_to_10_fulltable.csv', 'a')
        # writer = csv.writer(f)
        # header = ['id', 'question', 'answer', 'prediction', 'sql', 'response',  'r_num_cell', 't_num_cell']
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


                if tabsqlify == True:
                    sql_3 = """select * from T limit 3"""
                    three_row = sqldf(sql_3, locals())
                    three_row = table_linearization(three_row, style='pipe')
                    # print('\nThree example rows: \n', str(three_row))

                    sql, result, response, output_ans, linear_table = tabsqlify_wtq(T, title, tab_col, question, three_row, selection='rc')

                    t_num_cell = T.size
                    r_num_cell = result.size
                    print('R num_cell: ', r_num_cell, 'T num_cell: ', t_num_cell)

                else:
                    linear_table = table_linearization(T, style='pipe')
                    prompt_ans = gen_full_table_prompt(title, tab_col, linear_table, question)
                    # print(prompt_ans)
                    response = get_answer(prompt_ans)

                    try:
                        output_ans = response.split("Answer:")[1]
                        # print('Output answer: ', output_ans)
                    except:
                        print("Error: Answer generation.")
                        output_ans = "" + response
                    match = re.search(r'(The|the) answer is ([^\.]+)\.$', output_ans)
                    if match:
                        output_ans = match.group(2).strip('"')
                    t_num_cell = T.size
                    r_num_cell = T.size
                    sql = 'select * from T;'


                output_ans = output_ans.lower()
                print('\nResponse: ', response, '\nGen output: ', output_ans, 'Gold: ', answer)

                ## This is not official evaluation. ..... 
                if output_ans.strip() == answer or output_ans.strip().find(answer) != -1 \
                        or answer.strip().find(output_ans.strip()) != -1:
                    correct += 1
                    print("correct: ", correct)

                t_samples += 1

                print('Correcet: ', correct, 'total: ', t_samples, "Accuracy: ", correct / (t_samples + 0.0001))

                # ---------------------------------------------------------------------------------------------------------
                # tmp = {'key': ids, 'question': question, 'response': response, 'prediction': output_ans, 'answer': answer}
                # fw.write(json.dumps(tmp) + '\n')
                # #
                # data = [ids, question, answer, output_ans.strip(), sql, response,  r_num_cell, t_num_cell]
                # writer.writerow(data)

                # tmp = {'statement': dic['statement'], 'table_text': output_table_text, 'answer': dic['answer'], 'id': id, 'title': title}
                # fw.write(json.dumps(tmp) + '\n')
                # ---------------------------------------------------------------------------------------------------------

    # f.close()
    # fw.close()
    print('Final: Correcet: ', correct, 'total: ', t_samples, "Accuracy: ", correct / (t_samples + 0.0001))
    print('empty_error_ids: ', empty_error_ids)
# ----------------------------------------------------------------------------------------------

# Output 

#   warnings.warn('Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')


# id:  nu-507  Q:  who received more bronze medals: japan or south korea?  ans:  japan
# Table Column:  row_number, rank, nation, gold, silver, bronze, total
# Generate SQL for selecting the required rows and columns, given the question and table to answer the question correctly.
# SQLite table properties:

# Table: Marek Plawgo (row_number,year,competition,venue,position,event,notes)

# 3 example rows: 
#  select * from T limit 3;
# row_number | year | competition | venue | position | event | notes
# 0 | 1999 | european junior championships | riga, latvia | 4th | 400 m hurdles | 52.17
# 1 | 2000 | world junior championships | santiago, chile | 1st | 400 m hurdles | 49.23
# 2 | 2001 | world championships | edmonton, canada | 18th (sf) | 400 m hurdles | 49.8

# Q: when was his first 1st place record?
# SQL: select year from T where position = '1st' order by year asc limit 1

# SQLite table properties:

# Table: 2013–14 Toros Mexico season(row_number,game,day,date,kickoff,opponent,results_score,results_record,location,attendance)

# 3 example rows: 
#  select * from T limit 3;
# row_number | game | day | date | kickoff | opponent | results_score | results_record | location | attendance
# 0 | 1 | sunday | november 10 | t15:5 | at las vegas legends | l 3–7 | 0–1 | orleans arena | 1836
# 1 | 2 | sunday | november 17 | t13:5 | monterrey flash | l 6–10 | 0–2 | unisantos park | 363
# 2 | 3 | saturday | november 23 | t19:5 | at bay area rosal | w 10–7 | 1–2 | cabernet indoor sports | 652

# Q: what was the number of people attending the toros mexico vs. monterrey flash game?
# SQL: select attendance from T where opponent like '%monterrey flash%'

# SQLite table properties:

# Table: Radhika Pandit(row_number,year,film,role,language,notes)

# 3 example rows: 
#  select * from T limit 3;
# row_number | year | film | role | language | notes
# 0 | 2008 | moggina manasu | chanchala | kannada | filmfare award for best actress - kannada; karnataka state film award for best actress
# 1 | 2009 | olave jeevana lekkachaara | rukmini | kannada | innovative film award for best actress
# 2 | 2009 | love guru | kushi | kannada | filmfare award for best actress - kannada

# Q: what is the total number of films with the language of kannada listed?
# SQL: select film, language from T where language like '%kannada%'

# SQLite table properties:

# Table: List of storms on the Great Lakes(row_number,ship,type_of_vessel,lake,location,lives_lost)

# 3 example rows: 
#  select * from T limit 3;
# row_number | ship | type_of_vessel | lake | location | lives_lost
# 0 | argus | steamer | lake huron | 25 miles off kincardine, ontario | 25 lost
# 1 | james carruthers | steamer | lake huron | near kincardine | 18 lost
# 2 | hydrus | steamer | lake huron | near lexington, michigan | 28 lost

# Q: how many more ships were wrecked in lake huron than in erie?
# SQL: select ship, lake from T where lake like '%lake huron%' or lake like '%lake erie%'

# SQLite table properties:

# Table: Vidant Bertie Hospital(row_number,name,city,hospital_beds,operating_rooms,total,trauma_designation,affiliation,notes)

# 3 example rows: 
#  select * from T limit 3;
# row_number | name | city | hospital_beds | operating_rooms | total | trauma_designation | affiliation | notes
# 0 | alamance regional medical center | burlington | 238 | 15 | 253 | none | cone | none
# 1 | albemarle hospital | elizabeth city | 182 | 13 | 195 | none | vidant | none
# 2 | alexander hospital | hickory | 25 | 3 | 28 | none | none | none

# Q: what is the only hospital to have 6 hospital beds?
# SQL: select name, hospital_beds from T where hospital_beds = 6

# SQLite table properties:

# Table: Churnet Valley Railway(row_number,number,name,type,livery,status,notes)

# 3 example rows: 
#  select * from T limit 3;
# row_number | number | name | type | livery | status | notes
# 0 | none | brightside | yorkshire engine company 0-4-0 | black | under repair | currently dismantled for overhaul
# 1 | 6 | roger h. bennett | yorkshire engine company "janus" 0-6-0 | ncb blue | operational | ~
# 2 | d2334 | none | class 4 | green | under repair | stopped at 2012-9 diesel gala after failure

# Q: how many locomotives are currently operational?
# SQL: select name, status from T where status = 'operational'

# SQLite table properties:

# Table: 2012–13 Exeter City F.C. season(row_number,name,league,fa_cup,league_cup,jp_trophy,total)

# 3 example rows: 
#  select * from T limit 3;
# row_number | name | league | fa_cup | league_cup | jp_trophy | total
# 0 | scot bennett | 5 | 0 | 0 | 0 | 5
# 1 | danny coles | 3 | 0 | 0 | 0 | 3
# 2 | liam sercombe | 1 | 0 | 0 | 0 | 1

# Q: does pat or john have the highest total?
# SQL: select name, total from T where name like '%pat%' or name like '%john%'

# SQLite table properties:

# Table: The Harvest (Boondox album)(row_number, _, title, time, lyrics, music, producers, performers)

# 3 example rows: 
#  select * from T limit 3;
# row_number | _ | title | time | lyrics | music | producers | performers
# 0 | 1 | "intro" | 1:16 | none | none | none | none
# 1 | 2 | "7" | 3:30 | boondox | mike e. clark | boondox | boondox
# 2 | 3 | "out here" | 3:18 | boondox | mike e. clark; tino grosse | boondox | boondox

# Q: how many song come after "rollin hard"?
# SQL: select count(*) from T where row_number > (select row_number from T where title like '%rollin hard%')

# SQLite table properties:

# Table: GameStorm.org(row_number, iteration, dates, location, attendance, notes)

# 3 example rows: 
#  select * from T limit 3;
# row_number | iteration | dates | location | attendance | notes
# 0 | gamestorm 10 | 2008-3 | red lion - vancouver, wa | 750 | none
# 1 | gamestorm 11 | (2009-3-262009-3-29,p3d) | hilton - vancouver, wa | 736 | debut of video games, first-ever artist guest of honor, rob alexander
# 2 | gamestorm 12 | (2010-3-252010-3-28,p3d) | hilton - vancouver, wa | 802 | board games guest of honor: tom lehmann

# Q: what's the total attendance for gamestorm 11?
# SQL: select attendance, iteration from T where iteration = 'gamestorm 11'


# SQLite table properties:

# Table: 1981 Iowa Hawkeyes football team(row_number, date, opponent_, rank_, site, tv, result, attendance)

# 3 example rows: 
#  select * from T limit 3;
# row_number | date | opponent_ | rank_ | site | tv | result | attendance
# 0 | september 12 | #7 nebraska* | none | kinnick stadium • iowa city, ia | none | w 10-7 | 60160
# 1 | september 19 | at iowa state* | none | cyclone stadium • ames, ia (cy-hawk trophy) | none | l 12-23 | 53922
# 2 | september 26 | #6 ucla* | none | kinnick stadium • iowa city, ia | none | w 20-7 | 60004

# Q: which date had the most attendance?
# SQL: select date, attendance from T order by attendance desc


# SQLite table properties:

# Table: Figure skating at the Asian Winter Games (row_number, rank, nation, gold, silver, bronze, total)

# 3 example rows: 
#  select * from T limit 3;
# row_number | rank | nation | gold | silver | bronze | total
# 0 | 1 | china | 13 | 9 | 13 | 35
# 1 | 2 | japan | 7 | 10 | 7 | 24
# 2 | 3 | uzbekistan | 1 | 2 | 3 | 6

# Q: who received more bronze medals: japan or south korea?
# SQL:

# M1:  select nation, bronze from T where nation like '%japan%' or nation like '%south korea%' 

# promt_ans:
#  Based on the table title and execution result of the sql query bellow, find the answer to the given question correctly. 

# Table_title: Piotr Kędzia
# SQL: select Year, Venue, Position from T

# Year | Venue | Position
# 2001 | Debrecen, Hungary | 2nd
# 2001 | Debrecen, Hungary | 1st
# 2001 | Grosseto, Italy | 1st
# 2003 | Tampere, Finland | 3rd
# 2003 | Tampere, Finland | 2nd
# 2005 | Erfurt, Germany | 11th (sf)
# 2005 | Erfurt, Germany | 1st
# 2005 | Izmir, Turkey | 7th
# 2005 | Izmir, Turkey | 1st
# 2006 | Moscow, Russia | 2nd (h)
# 2006 | Gothenburg, Sweden | 3rd
# 2007 | Birmingham, United Kingdom | 3rd
# 2007 | Bangkok, Thailand | 7th
# 2007 | Bangkok, Thailand | 1st
# 2008 | Valencia, Spain | 4th
# 2008 | Beijing, China | 7th
# 2009 | Belgrade, Serbia | 2nd

# Question: in what city did piotr's last 1st place finish occur?
# A: To find the answer to this question, let’s think step by step.
# Based on the table, Piotr Kędzia's last 1st place finish occurred in angkok, Thailand in 2007. This is the most recent year in the table where he finished in 1st place. 
# Therefore, the answer is Bangkok, Thailand.
# Answer: Bangkok, Thailand

# Table_title: Playa de Oro International Airport
# SQL: select City, Passengers from T;

# City | Passengers
# United States, Los Angeles | 14,749
# United States, Houston | 5,465
# Canada, Calgary | 3,761
# Canada, Saskatoon | 2,282
# Canada, Vancouver | 2,103
# United States, Phoenix | 1,829
# Canada, Toronto | 1,202
# Canada, Edmonton | 110
# United States, Oakland | 107

# Question: how many more passengers flew to los angeles than to saskatoon from manzanillo airport in 2013?
# A: To find the answer to this question, let’s think step by step.
# Based on the table, in 2013, the number of passengers who flew to Los Angeles from Manzanillo Airport was 14,749, while the number of passengers who flew to Saskatoon was 2,282. 
# So, the difference in the number of passengers between Los Angeles and Saskatoon is 14,749 - 2,282 = 12,467. 
# Therefore, the answer is 12,467.
# Answer: 12,467


# Table_title: Figure skating at the Asian Winter Games
# SQL: select nation, bronze from T where nation like '%japan%' or nation like '%south korea%'

# nation | bronze
# japan | 7
# south korea | 2
# Question: who received more bronze medals: japan or south korea?
# A: To find the answer to this question, let’s think step by step.
# response:  Based on the table, Japan received 7 bronze medals while South Korea received 2 bronze medals. 
# Therefore, Japan received more bronze medals than South Korea.
# Answer: Japan

# Answer gen output:   Japan Gold:  japan
# R num_cell:  4 T num_cell:  49

# Response:  Based on the table, Japan received 7 bronze medals while South Korea received 2 bronze medals. 
# Therefore, Japan received more bronze medals than South Korea.
# Answer: Japan 
# Gen output:   japan Gold:  japan
# correct:  1
# Correcet:  1 total:  1 Accuracy:  0.9999000099990001
# Final: Correcet:  1 total:  1 Accuracy:  0.9999000099990001
# empty_error_ids:  []

# Process finished with exit code 0
