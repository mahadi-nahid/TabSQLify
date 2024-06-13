import json
from utils.preprocess import *
from utils.normalizer import *
import tiktoken

import json
import matplotlib.pyplot as plt


def count_tokens(prompt):

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # text = "This is an example sentence to count tokens."
    token_count = len(encoding.encode(prompt))
    # print(f"The text contains {token_count} tokens.")
    return token_count

def plot_histogram(jsonl_file, dataset):
    # Lists to store token counts
    token_counts = []

    # Read the JSONL file and extract token counts
    with open(jsonl_file, 'r') as infile:
        for line in infile:
            data = json.loads(line)
            token_count = data.get('token_count')  # Assuming 'token_count' is the attribute name
            if token_count is not None:  # Ensure the attribute exists
                token_counts.append(token_count)

    # Plotting the histogram
    plt.hist(token_counts, bins=30, color='blue', edgecolor='black', alpha=0.7)
    # plt.title('Token Count Histogram')
    plt.xlabel(f'Token Count ({dataset})')
    plt.ylabel('Frequency')
    plt.show()

def categorize_dataset(jsonl_file, threshold, dataset = 'wtq'):
    # Lists to store categories
    cut_0_to_10_percent = []
    cut_10_to_25_percent = []
    cut_25_to_50_percent = []
    cut_more_than_50_percent = []
    no_cut = []

    # Read the JSONL file and categorize data samples
    with open(jsonl_file, 'r') as infile:
        for line in infile:
            data = json.loads(line)
            token_count = data.get('token_count')  # Assuming 'token_count' is the attribute name
            if token_count is not None:  # Ensure the attribute exists
                if token_count > threshold:
                    cut_percentage = ((token_count - threshold) / token_count) * 100
                    if cut_percentage >= 0 and cut_percentage < 10:
                        cut_0_to_10_percent.append(data)
                    elif cut_percentage >= 10 and cut_percentage < 25:
                        cut_10_to_25_percent.append(data)
                    elif cut_percentage >= 25 and cut_percentage <= 50:
                        cut_25_to_50_percent.append(data)
                    else:
                        cut_more_than_50_percent.append(data)
                else:
                    no_cut.append(data)


    # Display the results
    print(f"Number of samples with 0-10% cut: {len(cut_0_to_10_percent)}")
    print(f"Number of samples with 10-20% cut: {len(cut_10_to_25_percent)}")
    print(f"Number of samples with 25-50% cut: {len(cut_25_to_50_percent)}")
    print(f"Number of samples with more than 50% cut: {len(cut_more_than_50_percent)}")
    print(f"Number of samples with no cut: {len(no_cut)}")

    # Save the categorized samples into different JSONL files
    save_to_jsonl(cut_0_to_10_percent, f'{dataset}_cut_0_to_10_percent.jsonl')
    save_to_jsonl(cut_10_to_25_percent, f'{dataset}_cut_10_to_25_percent.jsonl')
    save_to_jsonl(cut_25_to_50_percent, f'{dataset}_cut_25_to_50_percent.jsonl')
    save_to_jsonl(cut_more_than_50_percent, f'{dataset}_cut_more_than_50_percent.jsonl')
    save_to_jsonl(no_cut, f'{dataset}_no_cut.jsonl')


def save_to_jsonl(data, filename):
    with open(filename, 'w') as outfile:
        for item in data:
            json.dump(item, outfile)
            outfile.write('\n')


def prepare_data(input_file, output_file, dataset='wtq'):
    start = 2026
    end = start + 2500
    table_ids = list(range(start, end))

    # Read the input JSONL file and process each line
    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
        # for line in infile:
        for i, line in enumerate(infile):
            if i in table_ids:
                if i % 100 == 0:
                    print('i ----> ', i)

                data = json.loads(line)

                # fetaqa -----------------------------
                if dataset == 'fqa':
                    question = data['question'] # fetaqa
                    table = data['table_array'] # fetaqa
                    title = data['table_page_title'] # fetaqa
                    subtitle = data['table_section_title'] # feta =qa

                # tabfact -----------------------------
                if dataset == 'tf':
                    table = data['table_text']
                    question = data['statement']
                    title = data['table_caption']
                    data['id'] = i

                # wtq ---------------------------------
                if dataset == 'wtq':
                    table = data['table_text']
                    question = data['statement']
                    title = data['title']

                T = dict2df(table)
                T = T.assign(row_number=range(len(T)))
                row_number = T.pop('row_number')
                T.insert(0, 'row_number', row_number)
                T = convert_df_type(T)
                pt = table_linearization(T, style='pipe')
                # print('Title: ', title, '\nPiped Table: \n', pt)

                # prompt = title + '\n'+ subtitle + '\n' + pt + '\n'+ question
                prompt = title + '\n' + pt + '\n' + question

                token_count = count_tokens(prompt)
                print(token_count)
                data['token_count'] = token_count

                outfile.write(json.dumps(data) + '\n')

if __name__ == "__main__":

    # input_file = 'datasets/fetaQA-v1_test.jsonl'
    # output_file = 'fetaqa_experiment_data_1.jsonl'

    # input_file = 'datasets/tabfact_small_test.jsonl'
    # output_file = 'tabfact_experiment_data_1.jsonl'

    # input_file = 'datasets/wtq_test3.jsonl'
    output_file = 'wtq_experiment_data_1.jsonl'

    # dataset = ['wtq', 'fqa', 'tf']
    # prepare_data(input_file, output_file, dataset='tf')

    plot_histogram(output_file, 'WikiTableQuestion')

    threshold = 2000

    categorize_dataset(output_file, threshold, dataset='wtq')

    print("---end------")

# ---------------------

# tf, threshold  = 600
#
# Number of samples with 0-10% cut: 91
# Number of samples with 10-20% cut: 141
# Number of samples with 25-50% cut: 260
# Number of samples with more than 50% cut: 81
# Number of samples with no cut: 1451


# fqa, threshold = 600
# Number of samples with 0-10% cut: 81
# Number of samples with 10-20% cut: 143
# Number of samples with 25-50% cut: 202
# Number of samples with more than 50% cut: 69
# Number of samples with no cut: 1508

# wtq, threshold = 2000
# Number of samples with 0-10% cut: 76
# Number of samples with 10-20% cut: 89
# Number of samples with 25-50% cut: 116
# Number of samples with more than 50% cut: 128
# Number of samples with no cut: 3935


# # large_table_ids = [30, 44, 141, 158, 208, 237, 263, 279, 348, 367, 395, 401, 441, 444, 514, 546, 553, 573, 575, 642, 659, 690, 699, 718, 766, 904, 919, 936, 973, 999, 1004, 1008, 1014, 1041, 1073, 1084, 1109, 1140, 1166, 1185, 1259, 1330, 1365, 1382, 1406, 1430, 1453, 1596, 1617, 1624, 1627, 1671, 1707, 1844, 1873, 1877, 1895, 1899, 1918, 1945, 1955, 1969, 2019, 2047, 2100, 2160, 2191, 2212, 2219, 2235, 2243, 2292, 2293, 2323, 2355, 2359, 2439, 2443, 2504, 2552, 2565, 2630, 2633, 2650, 2673, 2696, 2729, 2797, 2816, 2819, 2900, 2906, 2908, 3040, 3092, 3139, 3158, 3203, 3228, 3253, 3290, 3294, 3419, 3434, 3469, 3487, 3573, 3624, 3662, 3663, 3679, 3693, 3706, 3709, 3711, 3732, 3750, 3941, 3990, 4004, 4007, 4068, 4085, 4188, 4194, 4196, 4222, 4299]
# # print(len(large_table_ids))
# # large_table_ids = large_table_ids[126:129]

