import pandas as pd

def read_excel_file(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=0)  # sheet_name=0 specifies the first sheet
    
    # Convert the data to a list of dictionaries, where each row is a dictionary
    data = df.to_dict(orient='records')
    
    return data