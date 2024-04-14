import streamlit as st
import pandas as pd
import os
import glob
import plotly.express as px
import json

csv_directory = 'csv_files'
list_file_path = 'predefined_lists.json'

# Ensure the directory for CSV files exists
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Load or initialize predefined lists
def load_lists():
    if os.path.exists(list_file_path):
        with open(list_file_path, 'r') as file:
            return json.load(file)
    else:
        return {
            "Big": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25],
            "Orph": [1, 20, 14, 31, 9, 17, 34, 6],
            "Small": [27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33]
        }

def save_lists(lists):
    with open(list_file_path, 'w') as file:
        json.dump(lists, file, indent=4)

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))

def analyze_continuous_sequences(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    sequences = {name: [] for name in lists.keys()}
    current_list = None
    current_count = 0

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

    return stats, numbers.tolist() 


def count_consecutive_triples(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    triple_counts = {name: 0 for name in lists.keys()}
    
    for list_name, list_numbers in lists.items():
        list_set = set(list_numbers)
        for i in range(len(numbers) - 2):
            if numbers[i] in list_set and numbers[i+1] in list_set and numbers[i+2] in list_set:
                triple_counts[list_name] += 1

    return triple_counts

def count_consecutive_doubles(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    double_counts = {name: 0 for name in lists.keys()}
    
    for list_name, list_numbers in lists.items():
        list_set = set(list_numbers)
        for i in range(len(numbers) - 1):
            if numbers[i] in list_set and numbers[i+1] in list_set:
                double_counts[list_name] += 1

    return double_counts

def count_numbers_by_list(file_path, lists):
    df = pd.read_csv(file_path)
    counts = {name: 0 for name in lists.keys()}
    for num in df['Number']:
        for list_name, numbers in lists.items():
            if num in numbers:
                counts[list_name] += 1
    return counts

def app():
    st.title('Analysis of Number Sequences')

    # Load or initialize lists
    lists = load_lists()

    # Manage lists section
    with st.expander("Manage Lists"):
        st.subheader("Add New List")
        new_list_name = st.text_input("Enter new list name:")
        number_selections = []
        for row in range(7):
            cols = st.columns(6)
            for i in range(6):
                idx = row * 6 + i
                if idx < 37:
                    with cols[i]:
                        if st.checkbox(f"{idx}", key=f"num_{idx}"):
                            number_selections.append(idx)

        st.subheader("Or Specify a Range")
        start_range = st.number_input("Start of Range", min_value=0, max_value=36, value=0)
        end_range = st.number_input("End of Range", min_value=0, max_value=36, value=36)
        
        if st.button("Add Range to List"):
            if new_list_name and start_range <= end_range:
                lists[new_list_name] = list(range(start_range, end_range + 1))
                save_lists(lists)
                st.success(f"List '{new_list_name}' added successfully with range from {start_range} to {end_range}.")
        
        if st.button("Add Individual Numbers to List"):
            if new_list_name and number_selections:
                lists[new_list_name] = number_selections
                save_lists(lists)
                st.success(f"List '{new_list_name}' added successfully with selected numbers.")

        delete_list_name = st.selectbox("Select a list to delete:", list(lists.keys()))
        if st.button("Delete List"):
            if delete_list_name in lists:
                del lists[delete_list_name]
                save_lists(lists)
                st.success(f"List '{delete_list_name}' deleted successfully.")

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

    # User selects which lists to analyze
    list_selection = st.multiselect("Select number lists to analyze:", list(lists.keys()))

    if st.button('Submit List Selection'):
        st.session_state.selected_lists = list_selection

    if 'selected_lists' in st.session_state and st.session_state.selected_lists:
        selected_lists = {name: lists[name] for name in st.session_state.selected_lists}
        if st.button('Show Analysis') and selected_file:
            counts = count_numbers_by_list(selected_file, selected_lists)
            data = pd.DataFrame({
                "List": list(selected_lists.keys()),
                "Count": [counts[name] for name in selected_lists]
            })
            data_pivot = data.melt(id_vars=["List"], value_vars=["Count"])
            fig = px.bar(data_pivot, x='variable', y='value', color='List', title="Number Distribution Across Lists",
                         barmode='stack', color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout(yaxis_title="Total Counts", xaxis_title="Lists")
            st.plotly_chart(fig)

            results = analyze_continuous_sequences(selected_file, selected_lists)
            for list_name, stats in results.items():
                st.subheader(f"List: {list_name}")
                with st.expander("Show sequences"):
                    st.write("Sequences:", stats['sequences'])
                st.write("Total series after first occurrence:", stats['total_series_after_first'])
                st.write("Average series length:", stats['average_series_length'])
                st.write(pd.DataFrame({
                    "Sequence Length": stats['sequences']
                }).transpose())

            triple_counts = count_consecutive_triples(selected_file, selected_lists)
            st.subheader("Count of Consecutive Triples")
            for list_name, count in triple_counts.items():
                st.write(f"{list_name}: {count} triples")

            double_counts = count_consecutive_doubles(selected_file, selected_lists)
            st.subheader("Count of Consecutive Doubles")
            for list_name, count in double_counts.items():
                st.write(f"{list_name}: {count} doubles")

if __name__ == "__main__":
    app()
