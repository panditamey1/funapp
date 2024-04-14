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

def group_after_nongroup_analysis(file_path):
    """Analyzes how many times a number from the predefined list follows a number not in the list."""
    df = pd.read_csv(file_path)
    counts = 0
    previous_num = None
    for num in df['Number']:
        if previous_num is not None and previous_num not in numbers_list and num in numbers_list:
            counts += 1
        previous_num = num
    return counts

# Streamlit user interface
st.title('Number Input and Analysis')

# File upload functionality
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_path = os.path.join(csv_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success('File uploaded successfully.')

# Creating or selecting a CSV file
new_file = st.text_input('Create a new CSV file (enter file name):')
create_button = st.button('Create')
existing_files = get_csv_files()
selected_file = st.selectbox('Or select an existing CSV file:', existing_files)

if create_button and new_file:
    file_path = create_new_csv(new_file)
    st.success(f'Created new file: {file_path}')
    selected_file = file_path

# File download link
if selected_file:
    st.write(f'You are working with: {selected_file}')
    st.download_button('Download CSV', data=pd.read_csv(selected_file).to_csv(index=False), file_name=os.path.basename(selected_file), mime='text/csv')

    if st.button('Show Analysis'):
        # Perform analysis and display results
        count = group_after_nongroup_analysis(selected_file)
        st.write(f'Numbers from the predefined group have occurred {count} times after numbers not in the group.')

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
    if 'selected_number' in st.session_state and st.session_state.selected_number is not None:
        num = st.session_state.selected_number
        save_number(num, selected_file)
        st.success(f'Number {num} saved!')
