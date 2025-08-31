import pandas as pd
import os

def missing(missing_list, student_list):
    """
    Remove missing students from the student list efficiently using set operations.
    """
    return list(set(student_list) - set(missing_list))

def run(el_list, ec_list, it_list, row, col):
    """
    Distribute students from three lists in a balanced way into a seating arrangement.
    """
    temp_matrix = []

    while el_list or ec_list or it_list:
        if ec_list:
            temp_matrix.append(ec_list.pop(0))
        if el_list:
            temp_matrix.append(el_list.pop(0))
        if it_list:
            temp_matrix.append(it_list.pop(0))

    matrix = []
    index = 0
    for i in range(row):
        row_data = []
        for j in range(col):
            if index < len(temp_matrix):
                row_data.append(temp_matrix[index])
                index += 1
            else:
                row_data.append('X')  # Placeholder for empty seats
        matrix.append(row_data)

    return list(map(list, zip(*matrix)))  # Transpose

def write(data, room_no):
    directory = "static/excel"
    os.makedirs(directory, exist_ok=True)

    file_path = f"{directory}/{room_no}.xlsx"
    
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, header=False)

def read(room_no):
    """
    Read the seating arrangement from an Excel file and replace NaN values with 'Blank'.
    """
    file_path = f'static/excel/{room_no}.xlsx'
    try:
        df = pd.read_excel(file_path, header=None)
        df.fillna("Blank", inplace=True)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame instead of None
