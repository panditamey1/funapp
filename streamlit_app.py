import streamlit as st
import pandas as pd
import os
import glob

csv_directory = 'csv_files'

# Ensure the directory for CSV files exists
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Default predefined list of numbers
default_numbers_list = [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25]
numbers_file_path = os.path.join(csv_directory, 'predefined_numbers.csv')

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))

def load_or_create_predefined_list():
    """Loads or creates a CSV file containing the predefined list of numbers."""
    if os.path.exists(numbers_file_path):
        df = pd.read_csv(numbers_file_path)
        return df['Number'].tolist()
    else:
        df = pd.DataFrame(default_numbers_list, columns=['Number'])
        df.to_csv(numbers_file_path, index=False)
        return default_numbers_list

def save_predefined_list(numbers_list):
    """Saves the predefined list of numbers to a CSV file."""
    df = pd.DataFrame(numbers_list, columns=['Number'])
    df.to_csv(numbers_file_path, index=False)

numbers_list = load_or_create_predefined_list()

# Streamlit user interface
st.title('Number Input and Analysis')

# Allow users to modify the predefined list of numbers
numbers_input = st.text_input('Modify the predefined list of numbers separated by commas:', ', '.join(map(str, numbers_list)))
if st.button('Update Predefined List'):
    try:
        new_numbers_list = [int(x.strip()) for x in numbers_input.split(',')]
        save_predefined_list(new_numbers_list)
        numbers_list = new_numbers_list
        st.success('Predefined list updated successfully.')
    except ValueError:
        st.error('Please enter valid integers separated by commas.')

# File management section...
# (Include file upload, selection, and download options as previously described)

# Example button logic using the predefined list for analysis or other purposes
if st.button('Perform Example Analysis'):
    st.write(f'Current predefined list: {numbers_list}')
    # Perform your analysis here using `numbers_list`

# This example does not include full file management code for brevity. You can integrate this section with file upload,
# file selection, saving numbers to selected file, and downloading the CSV file as described in previous examples.
