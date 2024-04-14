import streamlit as st
import pandas as pd
import os
import glob
import plotly.express as px

csv_directory = 'csv_files'

# Ensure the directory for CSV files exists
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))

def analyze_continuous_sequences(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    current_list = None
    current_count = 0
    sequences = {name: [] for name in lists.keys()}  # To store sequences of each list

    for number in numbers:
        found = False
        for list_name, list_numbers in lists.items():
            if number in list_numbers:
                if current_list == list_name:
                    current_count += 1
                else:
                    if current_list is not None:
                        sequences[current_list].append(current_count)
                    current_list = list_name
                    current_count = 1
                found = True
                break
        if not found and current_list is not None:
            sequences[current_list].append(current_count)
            current_list = None
            current_count = 0

    # Append the last sequence if it ended right at the end of the loop
    if current_count > 0:
        sequences[current_list].append(current_count)

    # Compute statistics for each list
    stats = {}
    for list_name, seqs in sequences.items():
        if seqs:
            total_series = len(seqs) - 1 if len(seqs) > 1 else 0
            avg_length = sum(seqs) / len(seqs)
        else:
            total_series = 0
            avg_length = 0
        stats[list_name] = {
            "sequences": seqs,
            "total_series_after_first": total_series,
            "average_series_length": avg_length
        }

    return stats

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
        "Orph": [1, 20, 14, 31, 9, 17, 34, 6],
        "Small": [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33]
    }

    if st.button('Show Analysis') and selected_file:
        # Perform analysis
        counts = count_numbers_by_list(selected_file, predefined_lists)
        data = pd.DataFrame({
            "List": ["Big", "Orph", "Small"],
            "Count": [counts["Big"], counts["Orph"], counts["Small"]]
        })

        # Pivot the data for a stacked bar chart
        data_pivot = data.melt(id_vars=["List"], value_vars=["Count"])

        # Create a stacked bar chart using Plotly
        fig = px.bar(data_pivot, x='variable', y='value', color='List', title="Number Distribution Across Lists",
                     barmode='stack', color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(yaxis_title="Total Counts", xaxis_title="Lists")

        # Display the figure
        st.plotly_chart(fig)
        results = analyze_continuous_sequences(selected_file, predefined_lists)
        for list_name, stats in results.items():
            st.subheader(f"List: {list_name}")
            st.write("Sequences:", stats['sequences'])
            st.write("Total series after first occurrence:", stats['total_series_after_first'])
            st.write("Average series length:", stats['average_series_length'])
            st.write(pd.DataFrame({
                "Sequence Length": stats['sequences']
            }).transpose())
if __name__ == "__main__":
    app()
