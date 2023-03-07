import gspread
from google.oauth2.service_account import Credentials

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


def update_sales_worksheet(data):
    '''
    Update worksheet with new data provided on new row.
    '''
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales workshet updated!\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)
