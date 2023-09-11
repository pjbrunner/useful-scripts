import argparse
import sys
from datetime import datetime

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description='Organize raw finances, spits out two files: dime_expenses.csv and dime_income.csv')
    parser.add_argument('file', help='CSV file containing income and expenses')
    parser.add_argument('-s', '--start_date', required=False, help='Start date for data subset of data, if no end date is specified today\'s date will be used. Format must be (YYYY-MM-DD)')
    parser.add_argument('-e', '--end_date', required=False, help='End date for data subset of data, must also specify a start date is using this parameter. Format must be (YYYY-MM-DD)')
    return parser.parse_args()

def create_data_frame(finance_file):
    df = pd.read_csv(finance_file)
    # Reverse lines.
    df = df[::-1]
    # Remove time of day from each transaction.
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    # Convert Date column to datetime64 objects. 
    df['Date'] = pd.to_datetime(df['Date'])
    # Change order of columns.
    df = df[['Type', 'Date', 'Amount', 'Category', 'Note']]

    return df

def get_date_subset(df, start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]

def split_note_column(df):
    # Split Note column into two columns using ':' as a delimiter.
    # https://stackoverflow.com/questions/14745022/how-to-split-a-dataframe-string-column-into-two-columns
    df[['Note', 'Expanded']] = df['Note'].str.split(':', n=1, expand=True)

def separate_income_and_expenses(df):
    # https://stackoverflow.com/questions/61784255/split-a-pandas-dataframe-into-two-dataframes-efficiently-based-on-some-condition
    condition = df.Type == 'Income'
    income = df[condition]
    expenses = df[~condition]

    return expenses, income

def is_date_format_good(day):
    try:
        datetime.strptime(day, '%Y-%m-%d')
    except ValueError as err:
        print(err)
        sys.exit(1)
    else:
        return True

def write_frames_to_file(expenses, income):
    if not expenses.empty:
        expenses.to_csv('dime_expenses.csv', columns=['Date', 'Amount', 'Category', 'Note', 'Expanded'], index=False)
    if not income.empty:
        income.to_csv('dime_income.csv', columns=['Date', 'Amount', 'Category', 'Note', 'Expanded'], index=False)

def main():
    args = get_args()

    df = create_data_frame(args.file)

    if args.start_date:
        is_date_format_good(args.start_date)
        if args.end_date:
            is_date_format_good(args.end_date)
        else:
            args.end_date = datetime.today().strftime('%Y-%m-%d')
        df = get_date_subset(df, args.start_date, args.end_date)

    split_note_column(df)
    expenses, income = separate_income_and_expenses(df)
    write_frames_to_file(expenses, income)

if __name__ == '__main__':
    main()