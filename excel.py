import pandas as pd

def extract_and_process_numbers(cell):
    # Check if cell contains space, indicating possible multiple entries
    if ' ' in cell:
        # Attempt to extract numbers from the cell
        try:
            # Split the cell by spaces and filter out valid numbers
            numbers = [str(int(x)) for x in cell.split() if x.isdigit()]
            #print(numbers)
            return numbers  # Concatenate the numbers with a space separator
        except ValueError:
            return cell  # Return original cell if conversion fails
    elif cell.isdigit():
        return int(cell)  # Return the number if the cell contains only a number

    else:
        return cell  # Return cell directly if no spaces or not handling numbers

# Load the Excel file
# df = pd.read_excel('Table_1.xlsx')
# read sheet 1
file_name = 'Table_1.xlsx'
df = pd.read_excel(file_name, sheet_name='Sheet', header=None)
# Convert all data to strings to avoid any data type issues during concatenation
df = df.astype(str)

# Create a new DataFrame to store the concatenated row
new_df = pd.DataFrame()

# Initialize an empty list to collect the concatenated data for each column
concatenated_data = []
matrix_df = pd.DataFrame()

# Loop through each row and process the data
for index, row in df.iterrows():
    matrix_concatenated_data = []    
    # check if all values are nan
    if all(pd.isna(row.values)):
        
        continue
    if all(row.values == 'nan'):
        continue
    print(row.values)
    for cell in row:
        #print(cell)
        # Extract and process numbers from each cell in the row
        numbers = extract_and_process_numbers(cell)
        if isinstance(numbers, list):
            concatenated_data.extend(numbers)
            matrix_concatenated_data.extend(numbers)
        else:
            if numbers != 'nan':
                concatenated_data.append(numbers)
                matrix_concatenated_data.append(numbers)
    # add each row to the matrix_df
    matrix_df = pd.concat([matrix_df, pd.DataFrame(matrix_concatenated_data).T], ignore_index=True)

    # processed_row = [extract_and_process_numbers(cell) for cell in row ]
    # flatten the list
    # processed_row = [item for sublist in processed_row for item in sublist ]
    # concatenated_data.append(processed_row)
# Convert the list to a DataFrame row
#new_df['Number'] = concatenated_data


# Save the new DataFrame to an Excel file
new_df.to_csv(f'{file_name.split(".")[0]}_concatenated.csv', index=False)
matrix_df.to_csv(f'{file_name.split(".")[0]}_matrix.csv', index=False)  