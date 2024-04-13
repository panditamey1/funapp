import streamlit as st
import pandas as pd
import os
import glob

# Predefined list of numbers
numbers_list = [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25]
csv_directory = 'csv_files'

# Ensure the directory for CSV files exists
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))

def create_new_csv(file_name):
    """Creates a new CSV file with the given name in the csv_directory."""
    file_path = os.path.join(csv_directory, file_name)
    if not file_path.endswith('.csv'):
        file_path += '.csv'
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['Number'])
        df.to_csv(file_path, index=False)
    return file_path

def save_number(num, file_path):
    df = pd.read_csv(file_path)
    new_row = pd.DataFrame({'Number': [num]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)

def analyze_number(num, file_path):
    df = pd.read_csv(file_path)
    count = df[df['Number'].isin([num])]['Number'].count()
    return count

def total_matches(file_path):
    df = pd.read_csv(file_path)
    matches = df[df['Number'].isin(numbers_list)].shape[0]
    total = df.shape[0]
    return matches, total

# Streamlit user interface
st.title('Number Input and Analysis')

# Creating or selecting a CSV file
new_file = st.text_input('Create a new CSV file (enter file name):')
create_button = st.button('Create')
existing_files = get_csv_files()
selected_file = st.selectbox('Or select an existing CSV file:', existing_files)

if create_button and new_file:
    file_path = create_new_csv(new_file)
    st.success(f'Created new file: {file_path}')
    selected_file = file_path

# If a file is selected or created, show the UI for number selection
if selected_file:
    st.write(f'You are working with: {selected_file}')

    # Initialize the selected number in session state if not already done
    if 'selected_number' not in st.session_state:
        st.session_state.selected_number = None

    # Layout the numbers in three rows
    numbers_per_row = 12
    for i in range(0, 37, numbers_per_row):
        cols = st.columns(numbers_per_row)
        for j in range(numbers_per_row):
            idx = i + j
            if idx > 36:
                break
            if cols[j].button(f'{idx}', key=f'num_{idx}'):
                st.session_state.selected_number = idx

    if st.button('Submit Number'):
        if st.session_state.selected_number is not None:
            num = st.session_state.selected_number
            save_number(num, selected_file)
            count = analyze_number(num, selected_file)
            matches, total = total_matches(selected_file)
            st.success(f'Number {num} saved!')
            st.info(f'The number {num} has appeared {count} times in the list.')
            st.info(f'Out of {total} entries, {matches} are in the predefined list.')
        else:
            st.error('Please select a number before submitting.')
