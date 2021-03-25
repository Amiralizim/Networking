import csv 
import pandas as pd

# This file is used for extracting the column names
def extract_columns(csvfile='Dataset-Unicauca-Version2-87Atts.csv'):
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        list_of_column_names = []

        for row in csv_reader:
            list_of_column_names.append(row)
            break
        
    print("List of column names: ", list_of_column_names)
    return list_of_column_names

# find the maximum value in each row for sql types
def extract_max(csvfile='Dataset-Unicauca-Version2-87Atts.csv', column_name='Flow.Duration'):
    df = pd.read_csv(csvfile)
    p=df[column_name].max()
    print("max value: ", p)

def format_column_names(csvfile='Dataset-Unicauca-Version2-87Atts.csv'):
    df = pd.read_csv(csvfile)
    extracted_columns = extract_columns(csvfile)
    list_of_column_names = []
    for columns in extracted_columns:
        list_of_column_names = columns
    # we need a dictionary of column names with keys being the old column names and values being 
    # the new ones
    columns = {}
    for column_name in list_of_column_names:
        columns[f'{column_name}'] = column_name.replace(".", "_")
    renamed_df = df.rename(columns=columns, inplace=True)
    renamed_df = df.to_csv('Dataset-Unicauca-Version2-87Atts.csv',index=None)
    extract_columns(csvfile)

csvfile = 'Dataset-Unicauca-Version2-87Atts.csv'
# column_name = 'Total.Length.of.Bwd.Packets'
# extract_max(csvfile, column_name)
# csvfile = 'Unicauca-dataset-April-June-2019-Network-flows.csv'
# extract_columns(csvfile)
format_column_names(csvfile)
