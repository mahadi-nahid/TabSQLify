from utils.preprocess import *
from utils.normalizer import *
import tiktoken


import warnings
warnings.filterwarnings('ignore')

start = 0
end = start + 100
table_ids = list(range(start, end))

def count_tokens(prompt):

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # text = "This is an example sentence to count tokens."
    token_count = len(encoding.encode(prompt))
    # print(f"The text contains {token_count} tokens.")
    return token_count

p_answer_wtq = """Based on the table information bellow, find the answer to the given question correctly. 

Table_title: Piotr Kędzia
Table:
Year | Venue | Position
2001 | Debrecen, Hungary | 2nd
2001 | Debrecen, Hungary | 1st
2001 | Grosseto, Italy | 1st
2003 | Tampere, Finland | 3rd
2003 | Tampere, Finland | 2nd
2005 | Erfurt, Germany | 11th (sf)
2005 | Erfurt, Germany | 1st
2005 | Izmir, Turkey | 7th
2005 | Izmir, Turkey | 1st
2006 | Moscow, Russia | 2nd (h)
2006 | Gothenburg, Sweden | 3rd
2007 | Birmingham, United Kingdom | 3rd
2007 | Bangkok, Thailand | 7th
2007 | Bangkok, Thailand | 1st
2008 | Valencia, Spain | 4th
2008 | Beijing, China | 7th
2009 | Belgrade, Serbia | 2nd

Question: in what city did piotr's last 1st place finish occur?
A: To find the answer to this question, let’s think step by step.
Based on the table, Piotr Kędzia's last 1st place finish occurred in angkok, Thailand in 2007. This is the most recent year in the table where he finished in 1st place. 
Therefore, the answer is Bangkok, Thailand.
Answer: Bangkok, Thailand

Table_title: Playa de Oro International Airport
Table:
City | Passengers
United States, Los Angeles | 14,749
United States, Houston | 5,465
Canada, Calgary | 3,761
Canada, Saskatoon | 2,282
Canada, Vancouver | 2,103
United States, Phoenix | 1,829
Canada, Toronto | 1,202
Canada, Edmonton | 110
United States, Oakland | 107

Question: how many more passengers flew to los angeles than to saskatoon from manzanillo airport in 2013?
A: To find the answer to this question, let’s think step by step.
Based on the table, in 2013, the number of passengers who flew to Los Angeles from Manzanillo Airport was 14,749, while the number of passengers who flew to Saskatoon was 2,282. 
So, the difference in the number of passengers between Los Angeles and Saskatoon is 14,749 - 2,282 = 12,467. 
Therefore, the answer is 12,467.
Answer: 12,467

"""

# print(count_tokens(p_answer_wtq))

# Create a function to count the number of cells in a DataFrame
def count_cells(dataframe):
    return dataframe.size

# Create an empty dictionary to store the frequency distribution
frequency_distribution = {
    '0-50': 0,
    '50-100': 0,
    '100-150': 0,
    '1500-200': 0,
    '200-250': 0,
    '250+': 0
}
long_tables = []

with open('../datasets/fetaQA-v1_test.jsonl', encoding='utf-8') as f1:
    for i, l in enumerate(f1):
        if i in table_ids:
            if i % 100 == 0:
                print('i ----> ', i)
            dic = json.loads(l)
            # id = dic['ids']
            id = dic['feta_id']
            # table = dic['table_text']
            table = dic['table_array']
            question = dic['statement']
            # answer = dic['label']
            # answer = ','.join(answer)
            # answer = answer.lower()
            # title = dic['table_caption']
            T = dict2df(table)
            T = T.assign(row_number=range(len(T)))
            row_number = T.pop('row_number')
            T.insert(0, 'row_number', row_number)
            tab_coll = T.columns
            # print('Columns: ', tab_coll)

            # print('\n\nid: ', id, ' Q: ', question, ' ans: ', answer)
            T = convert_df_type(T)
            # print('W:\n\n', T)

            pt = table_linearization(T, style='pipe')
            # print('Title: ', title, '\nPiped Table: \n', pt)
            #

            pt = question + pt
            
            # print('id: ', id)
            row, col = T.shape
            num_cell = T.size
            # print('#Row: ', row, '#Col: ', col, '#Cell: ', num_cell)

            cell_count = count_cells(T)
            token_count = count_tokens(pt)
            # print("Number of tokens: ", token_count)

            if token_count > 1500:
                long_tables.append(id)

            # Update the frequency distribution based on cell count range
            if cell_count < 50:
                frequency_distribution['0-50'] += 1
            elif cell_count < 100:
                frequency_distribution['50-100'] += 1
            elif cell_count < 150:
                frequency_distribution['100-150'] += 1
            elif cell_count < 200:
                frequency_distribution['1500-200'] += 1
                long_tables.append(id)
            elif cell_count < 250:
                frequency_distribution['200-250'] += 1
                long_tables.append(id)
            else:
                frequency_distribution['250+'] += 1
                long_tables.append(id)

# Print the frequency distribution
for key, value in frequency_distribution.items():
    print(f'Number of tables with cell count in {key}: {value}')

print('Large tables: ', long_tables, '\n#large_table:', len(long_tables))
print('\n******End.******')


# Number of DataFrames with cell count in 0-100: 1878
# Number of DataFrames with cell count in 100-200: 951
# Number of DataFrames with cell count in 200-300: 327
# Number of DataFrames with cell count in 300-400: 0
# Number of DataFrames with cell count in 400-500: 136
# Number of DataFrames with cell count in 500+: 142
# Large tables:  ['nu-10', 'nu-14', 'nu-18', 'nu-30', 'nu-34', 'nu-44', 'nu-65', 'nu-114', 'nu-116', 'nu-125', 'nu-141', 'nu-158', 'nu-166', 'nu-175', 'nu-180', 'nu-208', 'nu-237', 'nu-244', 'nu-263', 'nu-265', 'nu-266', 'nu-274', 'nu-279', 'nu-310', 'nu-319', 'nu-325', 'nu-348', 'nu-367', 'nu-395', 'nu-401', 'nu-434', 'nu-441', 'nu-443', 'nu-444', 'nu-455', 'nu-458', 'nu-490', 'nu-514', 'nu-527', 'nu-546', 'nu-553', 'nu-567', 'nu-569', 'nu-573', 'nu-575', 'nu-585', 'nu-619', 'nu-630', 'nu-642', 'nu-659', 'nu-664', 'nu-666', 'nu-676', 'nu-690', 'nu-696', 'nu-699', 'nu-719', 'nu-723', 'nu-732', 'nu-736', 'nu-751', 'nu-754', 'nu-759', 'nu-766', 'nu-788', 'nu-793', 'nu-811', 'nu-863', 'nu-867', 'nu-871', 'nu-872', 'nu-884', 'nu-887', 'nu-893', 'nu-904', 'nu-919', 'nu-922', 'nu-928', 'nu-936', 'nu-941', 'nu-973', 'nu-974', 'nu-983', 'nu-999', 'nu-1004', 'nu-1008', 'nu-1014', 'nu-1016', 'nu-1041', 'nu-1049', 'nu-1051', 'nu-1055', 'nu-1060', 'nu-1073', 'nu-1084', 'nu-1088', 'nu-1091', 'nu-1109', 'nu-1134', 'nu-1140', 'nu-1149', 'nu-1151', 'nu-1179', 'nu-1185', 'nu-1188', 'nu-1225', 'nu-1251', 'nu-1252', 'nu-1259', 'nu-1262', 'nu-1270', 'nu-1275', 'nu-1289', 'nu-1300', 'nu-1321', 'nu-1335', 'nu-1356', 'nu-1365', 'nu-1382', 'nu-1406', 'nu-1426', 'nu-1430', 'nu-1433', 'nu-1446', 'nu-1448', 'nu-1453', 'nu-1481', 'nu-1505', 'nu-1560', 'nu-1567', 'nu-1569', 'nu-1579', 'nu-1605', 'nu-1617', 'nu-1624', 'nu-1627', 'nu-1665', 'nu-1667', 'nu-1669', 'nu-1671', 'nu-1685', 'nu-1697', 'nu-1707', 'nu-1719', 'nu-1764', 'nu-1786', 'nu-1790', 'nu-1844', 'nu-1863', 'nu-1864', 'nu-1873', 'nu-1877', 'nu-1895', 'nu-1899', 'nu-1918', 'nu-1927', 'nu-1945', 'nu-1947', 'nu-1954', 'nu-1969', 'nu-1977', 'nu-2003', 'nu-2019', 'nu-2043', 'nu-2047', 'nu-2082', 'nu-2096', 'nu-2100', 'nu-2108', 'nu-2160', 'nu-2168', 'nu-2191', 'nu-2210', 'nu-2219', 'nu-2228', 'nu-2235', 'nu-2243', 'nu-2264', 'nu-2283', 'nu-2292', 'nu-2293', 'nu-2295', 'nu-2302', 'nu-2303', 'nu-2317', 'nu-2353', 'nu-2355', 'nu-2359', 'nu-2429', 'nu-2439', 'nu-2443', 'nu-2445', 'nu-2466', 'nu-2489', 'nu-2504', 'nu-2510', 'nu-2529', 'nu-2552', 'nu-2560', 'nu-2565', 'nu-2569', 'nu-2585', 'nu-2591', 'nu-2600', 'nu-2609', 'nu-2630', 'nu-2633', 'nu-2650', 'nu-2653', 'nu-2657', 'nu-2696', 'nu-2706', 'nu-2722', 'nu-2724', 'nu-2726', 'nu-2729', 'nu-2749', 'nu-2758', 'nu-2779', 'nu-2797', 'nu-2801', 'nu-2803', 'nu-2811', 'nu-2816', 'nu-2819', 'nu-2820', 'nu-2822', 'nu-2829', 'nu-2830', 'nu-2832', 'nu-2844', 'nu-2861', 'nu-2866', 'nu-2870', 'nu-2878', 'nu-2880', 'nu-2882', 'nu-2900', 'nu-2906', 'nu-2908', 'nu-2919', 'nu-2931', 'nu-2952', 'nu-2957', 'nu-2975', 'nu-3017', 'nu-3036', 'nu-3040', 'nu-3042', 'nu-3053', 'nu-3083', 'nu-3115', 'nu-3139', 'nu-3141', 'nu-3158', 'nu-3203', 'nu-3213', 'nu-3228', 'nu-3246', 'nu-3249', 'nu-3253', 'nu-3260', 'nu-3275', 'nu-3281', 'nu-3285', 'nu-3290', 'nu-3294', 'nu-3299', 'nu-3301', 'nu-3304', 'nu-3312', 'nu-3341', 'nu-3346', 'nu-3358', 'nu-3372', 'nu-3419', 'nu-3420', 'nu-3430']
# #large_table: 278

# token_count > 4000
# Large tables:  ['nu-30', 'nu-44', 'nu-141', 'nu-158', 'nu-208', 'nu-237', 'nu-263', 'nu-279', 'nu-348', 'nu-367', 'nu-395', 'nu-401', 'nu-441', 'nu-444', 'nu-514', 'nu-546', 'nu-553', 'nu-573', 'nu-575', 'nu-642', 'nu-659', 'nu-690', 'nu-699', 'nu-718', 'nu-766', 'nu-904', 'nu-919', 'nu-936', 'nu-973', 'nu-999', 'nu-1004', 'nu-1008', 'nu-1014', 'nu-1041', 'nu-1073', 'nu-1084', 'nu-1109', 'nu-1140', 'nu-1166', 'nu-1185', 'nu-1259', 'nu-1330', 'nu-1365', 'nu-1382', 'nu-1406', 'nu-1430', 'nu-1453', 'nu-1596', 'nu-1617', 'nu-1624', 'nu-1627', 'nu-1671', 'nu-1707', 'nu-1844', 'nu-1873', 'nu-1877', 'nu-1895', 'nu-1899', 'nu-1918', 'nu-1945', 'nu-1955', 'nu-1969', 'nu-2019', 'nu-2047', 'nu-2100', 'nu-2160', 'nu-2191', 'nu-2212', 'nu-2219', 'nu-2235', 'nu-2243', 'nu-2292', 'nu-2293', 'nu-2323', 'nu-2355', 'nu-2359', 'nu-2439', 'nu-2443', 'nu-2504', 'nu-2552', 'nu-2565', 'nu-2630', 'nu-2633', 'nu-2650', 'nu-2673', 'nu-2696', 'nu-2729', 'nu-2797', 'nu-2816', 'nu-2819', 'nu-2900', 'nu-2906', 'nu-2908', 'nu-3040', 'nu-3092', 'nu-3139', 'nu-3158', 'nu-3203', 'nu-3228', 'nu-3253', 'nu-3290', 'nu-3294', 'nu-3419', 'nu-3434', 'nu-3469', 'nu-3487', 'nu-3573', 'nu-3624', 'nu-3662', 'nu-3663', 'nu-3679', 'nu-3693', 'nu-3706', 'nu-3709', 'nu-3711', 'nu-3732', 'nu-3750', 'nu-3941', 'nu-3990', 'nu-4004', 'nu-4007', 'nu-4068', 'nu-4085', 'nu-4188', 'nu-4194', 'nu-4196', 'nu-4222', 'nu-4299']
# large_table: 128
# larg_table_ids = [30, 44, 141, 158, 208, 237, 263, 279, 348, 367, 395, 401, 441, 444, 514, 546, 553, 573, 575, 642, 659, 690, 699, 718, 766, 904, 919, 936, 973, 999, 1004, 1008, 1014, 1041, 1073, 1084, 1109, 1140, 1166, 1185, 1259, 1330, 1365, 1382, 1406, 1430, 1453, 1596, 1617, 1624, 1627, 1671, 1707, 1844, 1873, 1877, 1895, 1899, 1918, 1945, 1955, 1969, 2019, 2047, 2100, 2160, 2191, 2212, 2219, 2235, 2243, 2292, 2293, 2323, 2355, 2359, 2439, 2443, 2504, 2552, 2565, 2630, 2633, 2650, 2673, 2696, 2729, 2797, 2816, 2819, 2900, 2906, 2908, 3040, 3092, 3139, 3158, 3203, 3228, 3253, 3290, 3294, 3419, 3434, 3469, 3487, 3573, 3624, 3662, 3663, 3679, 3693, 3706, 3709, 3711, 3732, 3750, 3941, 3990, 4004, 4007, 4068, 4085, 4188, 4194, 4196, 4222, 4299]


# token_count > 3500
# Large tables:  [18, 30, 44, 141, 158, 208, 237, 263, 279, 348, 367, 395, 401, 434, 441, 444, 514, 546, 553, 573, 575, 585, 642, 659, 690, 699, 718, 766, 904, 919, 936, 973, 999, 1004, 1008, 1014, 1041, 1073, 1084, 1109, 1140, 1166, 1185, 1259, 1330, 1365, 1382, 1406, 1430, 1453, 1579, 1596, 1617, 1624, 1627, 1671, 1707, 1844, 1873, 1877, 1895, 1899, 1918, 1945, 1955, 1969, 2019, 2047, 2100, 2160, 2191, 2212, 2219, 2228, 2235, 2243, 2292, 2293, 2323, 2353, 2355, 2359, 2439, 2443, 2504, 2529, 2552, 2565, 2609, 2630, 2633, 2650, 2673, 2696, 2724, 2729, 2797, 2803, 2816, 2819, 2870, 2900, 2906, 2908, 3040, 3092, 3139, 3158, 3203, 3228, 3253, 3290, 3294, 3419, 3420, 3434, 3469, 3487, 3573, 3624, 3662, 3663, 3679, 3693, 3706, 3709, 3711, 3732, 3750, 3826, 3941, 3972, 3990, 4004, 4007, 4068, 4085, 4188, 4194, 4196, 4222, 4299]
#large_table: 142



# i ---->  0 Tabfact

# Number of tables with cell count in 0-50: 11
# Number of tables with cell count in 50-100: 61
# Number of tables with cell count in 100-150: 9
# Number of tables with cell count in 1500-200: 0
# Number of tables with cell count in 200-250: 10
# Number of tables with cell count in 250+: 9
# Large tables:  [25, <built-in function id>, 26, <built-in function id>, 27, <built-in function id>, 28, <built-in function id>, 29, <built-in function id>, 30, <built-in function id>, 31, <built-in function id>, 32, <built-in function id>, 33, <built-in function id>, 34, <built-in function id>, 61, 62, 63, 64, 65, 78, 79, 80, 81, 82, <built-in function id>, 83, <built-in function id>, 84, <built-in function id>, 85, <built-in function id>, 86, <built-in function id>, 87, <built-in function id>, 88, <built-in function id>, 89, <built-in function id>, 90, <built-in function id>]
# #large_table: 47
#
# ******End.******

# i ---->  0 FetaQA
# Number of tables with cell count in 0-50: 38
# Number of tables with cell count in 50-100: 24
# Number of tables with cell count in 100-150: 25
# Number of tables with cell count in 1500-200: 8
# Number of tables with cell count in 200-250: 0
# Number of tables with cell count in 250+: 5
# Large tables:  [21418, 20853, 16730, 12617, 11595, 2034, 1804, 21526, 20887, 14571, 11319, 945, 12409]
# #large_table: 13
#
# ******End.******



# larg_table_ids =
# Binder chatgpt acc: 2410/4344 = 0.55478821362

