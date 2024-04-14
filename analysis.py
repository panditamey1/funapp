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


def count_numbers_by_list(file_path, lists):
    """Count occurrences of numbers from each predefined list in the file."""
    df = pd.read_csv(file_path)
    counts = {name: 0 for name in lists.keys()}
    for num in df['Number']:
        for list_name, numbers in lists.items():
            if num in numbers:
                counts[list_name] += 1
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
        "Big": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25],
        "Orpha": [1, 20, 14, 31, 9, 17, 34, 6],
        "Small": [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33]
    }

    if st.button('Show Analysis') and selected_file:
        # Perform analysis
        counts = count_numbers_by_list(selected_file, predefined_lists)
        # Display results as a bar chart
        st.bar_chart(counts)

if __name__ == "__main__":
    app()
