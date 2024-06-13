import ast
import os
from typing import Dict, List
import pandas as pd

## Adapted from Binder and Dater paper 

def dict2df(table: Dict, add_row_id=False, lower_case=True):
    """
    Dict to pd.DataFrame.
    tapex format.
    """
    header, rows = table[0], table[1:]
    # print('header before : ', header)
    header = preprocess_columns(header)
    # print('header after: ', header)
    df = pd.DataFrame(data=rows, columns=header)
    return df


def table_linearization(table: pd.DataFrame, style: str = 'pipe'):
    """
    linearization table according to format.
    """
    assert style in ['pipe', 'row_col']
    linear_table = ''
    if style == 'pipe':
        header = ' | '.join(table.columns) + '\n'
        linear_table += header
        rows = table.values.tolist()
        # print('header: ', linear_table)
        # print(rows)
        for row_idx, row in enumerate(rows):
            # print(row)
            line = ' | '.join(str(v) for v in row)
            # print('line: ', line)
            if row_idx != len(rows) - 1:
                line += '\n'
            linear_table += line

    elif style == 'row_col':
        header = 'col : ' + ' | '.join(table.columns) + '\n'
        linear_table += header
        rows = table.values.tolist()
        for row_idx, row in enumerate(rows):
            line = 'row {} : '.format(row_idx + 1) + ' | '.join(row)
            if row_idx != len(rows) - 1:
                line += '\n'
            linear_table += line
    return linear_table


def strip_tokens(table_string, sep):
    rows = table_string.strip().split('\n')
    stripped_data = []
    for row in rows:
        tokens = row.split('|')
        stripped_tokens = [token.strip() for token in tokens]
        stripped_data.append(stripped_tokens)

    formatted_table = []
    for row in stripped_data:
        formatted_row = sep.join(row)
        formatted_table.append(formatted_row)

    return '\n'.join(formatted_table)


def preprocess_columns(columns):
    # columns = table.split('\n')[0].split('|')
    # print('preprocessing columns')
    tab_coll = []
    illegal_chars_1 = [' ', '/', '\\', '-', ':', '#', '%']
    illegal_chars_2 = ['.', '(', ')', '[', ']', '{', '}', '*', '$', ',', '?', '!', '\'', '$', '@', '&', '=',
                       '+']
    for x in columns:
        x = x.strip()
        # print(x)
        if x.isnumeric():
            x = "_" + x
        x = x.replace(">", "GT")
        x = x.replace("<", "LT")
        x = x.replace("\\n", "_")
        x = x.replace("\n", "_")
        x = x.replace('\\', '_')
        for char in illegal_chars_1:
            x = x.replace(char, '_')
        for char in illegal_chars_2:
            x = x.replace(char, '')
        tab_coll.append(x.strip())

    counts = {}
    preprocessed_colls = []
    for item in tab_coll:
        if item in counts:
            counts[item] += 1
            preprocessed_colls.append(f"{item}{counts[item]}")
        else:
            counts[item] = 0
            preprocessed_colls.append(item)

    return preprocessed_colls


def extract_elements_from_string(string_list):
    try:
        # Safely evaluate the string as a Python expression
        elements = ast.literal_eval(string_list)

        if isinstance(elements, list):
            return elements
        else:
            return []
    except (SyntaxError, ValueError):
        return []


def count_cells(table: str) -> int:
    rows = table.split('\n')
    cell_count = 0
    for row in rows:
        cells = row.split('|')
        cell_count += len(cells)
    return cell_count
