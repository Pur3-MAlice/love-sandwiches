import gspread
from google.oauth2.service_account import Credentials
# from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    '''
    Get sales data from the user. run while loop to ensure correct data input
    data must be 6 int seperated by commas, while loop will run until valid.
    '''
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 12,34,45,63,67,45\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is Valid!\n")
            break

    return sales_data


def validate_data(values):
    '''
    Inside the try, converts all string into integers.
    Raises Error if string cant be converted, or if not 6 ints
    '''
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    '''
    Recivies list of integers to be insterted into a worksheet 
    update the relevant worksheet with the data
    '''
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated!\n")


def calculate_surplus(sales_row):
    '''
    Compare sales with stock and calculate the surple for each item type.
    The surplus is defined as the sales figure subbed from the stock:
    - Pos surplus = waste
    - neg surplus = not enough stock 
    '''
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    '''
    Collects columns of data from slaes worksheet, colleccting
    the last 5 entries for each sandwich adn returns the data
    as a list of lists
    '''
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    '''
    Calc av stock for each item type, add 10%
    '''
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column) 
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    '''
    Run all prog functions
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()