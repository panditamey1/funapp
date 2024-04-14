import streamlit as st
import pandas as pd
import os
import os
import glob

csv_directory = 'csv_files'

# Ensure the directory for CSV files exists
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))

def group_after_nongroup_analysis(file_path, numbers_list):
    """Analyzes how many times a number from the predefined list follows a number not in the list."""
    df = pd.read_csv(file_path)
    counts = 0
    previous_num = None
    for num in df['Number']:
        if previous_num is not None and previous_num not in numbers_list and num in numbers_list:
            counts += 1
        previous_num = num
    return counts

def app():
    st.title('Analysis of Number Sequences')

    # File upload functionality
    uploaded_file = st.file_uploader("Upload a CSV file for analysis", type=['csv'])
    if uploaded_file is not None:
        file_path = os.path.join(csv_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success('File uploaded successfully. You can now select it below for analysis.')

    # Select CSV file for analysis
    existing_files = get_csv_files()
    selected_file = st.selectbox('Or select an existing CSV file:', existing_files)

    # Predefined lists
    predefined_lists = {
        "List 1": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25],
        "List 2": [1, 20, 14, 31, 9, 17, 34, 6],
        "List 3": [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33],
        "Custom": []
    }

    # Dropdown for selecting predefined list
    selected_list_name = st.selectbox('Choose a predefined list or select custom to define your own:', list(predefined_lists.keys()))
    numbers_list = predefined_lists[selected_list_name]

    # Allow for custom list input if 'Custom' is selected
    if selected_list_name == 'Custom':
        custom_input = st.text_area('Enter a custom list of numbers separated by commas (e.g., 5, 11, 16):')
        try:
            numbers_list = [int(x.strip()) for x in custom_input.split(',')]
            if custom_input:  # Only display the message if input is not empty
                st.success('Custom list accepted.')
        except ValueError:
            st.error('Please enter valid integers separated by commas.')
            numbers_list = []

    # Button to show analysis
    if st.button('Show Analysis') and numbers_list and selected_file:
        # Perform analysis and display results
        count = group_after_nongroup_analysis(selected_file, numbers_list)
        st.write(f'Numbers from the selected group have occurred {count} times after numbers not in the group.')

# Run the app function to start Streamlit app
if __name__ == "__main__":
    app()
