import pandas as pd

def missing(missing_list, student_list):
    """
    Remove missing students from the student list.
    Uses set operations for better efficiency.
    """
    return list(set(student_list) - set(missing_list))


def run(el_list, ec_list, it_list, col, row):
    """
    Generate a seating arrangement based on the given student lists.
    - Uses a more efficient approach to distribute students in a zigzag pattern.
    """
    temp_matrix = []
    
    # Ensuring students are evenly distributed
    while el_list or ec_list or it_list:
        if it_list:
            temp_matrix.append(it_list.pop(0))
        if ec_list:
            temp_matrix.append(ec_list.pop(0))
        if el_list:
            temp_matrix.append(el_list.pop(0))

    # Convert temp_matrix into a row-column matrix
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

    # Transpose to match the expected format
    return list(map(list, zip(*matrix)))


def write(result, room_no):
    """
    Write the seating arrangement to an Excel file.
    """
    file_path = f'static/excel/{room_no}.xlsx'
    df = pd.DataFrame(result)
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=room_no, header=None, index=False)


def read(room_no):
    """
    Read the seating arrangement from an Excel file.
    Includes error handling in case the file is missing.
    """
    file_path = f'static/excel/{room_no}.xlsx'
    try:
        return pd.read_excel(file_path, header=None, index_col=False)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
