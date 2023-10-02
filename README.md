# useful-scripts

## organize_dime.py

Organizes output from a budget tracking iOS app called [Dime](https://apps.apple.com/us/app/dime-budgets-and-expenses/id1635280255). Dime can export all transactions to a CSV file, that file is a required argument for the script. Dime includes the date as well as the exact time each transaction is logged and lets you add a short description. This script spits out a CSV file in the current directory called `dime_expenses.csv` with all expenses and if you put income into Dime a separate file called `dime_income.csv` with all income will be produced.
  
I like having a description of the transaction in addition to the recipient. So when you enter a description in Dime if you specify a recipient then add a ':' and give a short description this script will split those into separate columns. The recipient is put in a category called "Note" and the description is put in a "Expanded" category.
  
You can enter a date range using the start_date and end_date parameters using YYYY-MM-DD format. If you enter a start_date with no end_date the current date will be used as the end_date. If you don't give a start_date or end_date then all transactions in the input_file will be organized. If an end_date is given with no start_date then the script will treat it like no date range was given so all transactions will be organized.

### Usage:

```
usage: organize_dime.py [-h] [-s START_DATE] [-e END_DATE] input_file

Organize raw finances, spits out two files: dime_expenses.csv and dime_income.csv

positional arguments:
  input_file            CSV file containing income and expenses

options:
  -h, --help            show this help message and exit
  -s START_DATE, --start_date START_DATE
                        Start date for data subset of data, if no end date is specified today's date will be used. Format must be (YYYY-MM-DD)
  -e END_DATE, --end_date END_DATE
                        End date for data subset of data, must also specify a start date is using this parameter. Format must be (YYYY-MM-DD)
```

Python Version: 3.11.5