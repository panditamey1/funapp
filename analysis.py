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
def get_consecutive_sequences(file_path, numbers_list):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Assume the CSV has a single column named 'Number' containing the numbers
    numbers = df['Number'].tolist()
    
    sequences = []  # This will hold the list of sequences found
    current_sequence = []  # Temporary storage for the current sequence

    # Iterate over the numbers in the CSV
    for number in numbers:
        if number in numbers_list:
            # If the number is in the list, add to the current sequence
            current_sequence.append(number)
        else:
            # If the number is not in the list, check if there was an ongoing sequence
            if current_sequence:
                # If there was a sequence, add it to the sequences list and reset
                sequences.append(current_sequence)
                current_sequence = []  # Reset the current sequence
    
    # Check if there's an unfinished sequence at the end of the file
    if current_sequence:
        sequences.append(current_sequence)
    
    return sequences

def analyze_and_extract_sequences(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    sequences = {name: [] for name in lists.keys()}
    actual_sequences = {name: [] for name in lists.keys()}
    consecutive_doubles = {name: 0 for name in lists.keys()}
    failed_doubles = {name: 0 for name in lists.keys()}
    consecutive_triples = {name: 0 for name in lists.keys()}
    failed_triples = {name: 0 for name in lists.keys()}
    double_sequences = {name: [] for name in lists.keys()}
    triple_sequences = {name: [] for name in lists.keys()}
    failed_double_sequences = {name: [] for name in lists.keys()}
    failed_triple_sequences = {name: [] for name in lists.keys()}
    current_list = None
    current_sequence = []

    for i, number in enumerate(numbers):
        found = False
        for list_name, list_numbers in lists.items():
            if number in list_numbers:
                if current_list == list_name:
                    current_sequence.append(number)
                    if len(current_sequence) == 2:
                        consecutive_doubles[list_name] += 1
                        double_sequences[list_name].append(list(current_sequence))
                    elif len(current_sequence) >= 3:
                        consecutive_triples[list_name] += 1
                        triple_sequences[list_name].append(list(current_sequence[:3]))
                        current_sequence = current_sequence[-2:]  # Start new sequence potentially
                else:
                    if current_list is not None and len(current_sequence) >= 2:
                        if len(current_sequence) == 2:
                            failed_doubles[current_list] += 1
                            failed_double_sequences[current_list].append(list(current_sequence))
                        elif len(current_sequence) == 3:
                            failed_triples[current_list] += 1
                            failed_triple_sequences[current_list].append(list(current_sequence))
                    current_list = list_name
                    current_sequence = [number]
                found = True
                break
        if not found and current_list is not None:
            if len(current_sequence) == 2:
                failed_doubles[current_list] += 1
                failed_double_sequences[current_list].append(list(current_sequence))
            elif len(current_sequence) == 3:
                failed_triples[current_list] += 1
                failed_triple_sequences[current_list].append(list(current_sequence))
            current_list = None
            current_sequence = []

    if current_sequence:
        sequences[current_list].append(len(current_sequence))
        actual_sequences[current_list].append(current_sequence)

    stats = {}
    for list_name, seqs in sequences.items():
        stats[list_name] = {
            "sequences": seqs,
            "actual_sequences": actual_sequences[list_name],
            "consecutive_doubles": consecutive_doubles[list_name],
            "failed_doubles": failed_doubles[list_name],
            "consecutive_triples": consecutive_triples[list_name],
            "failed_triples": failed_triples[list_name],
            "double_sequences": double_sequences[list_name],
            "triple_sequences": triple_sequences[list_name],
            "failed_double_sequences": failed_double_sequences[list_name],
            "failed_triple_sequences": failed_triple_sequences[list_name]
        }

    return stats, numbers.tolist()


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
def failed_consecutive_doubles(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    failed_double_counts = {name: 0 for name in lists.keys()}

    for list_name, list_numbers in lists.items():
        list_set = set(list_numbers)
        for i in range(len(numbers) - 1):
            # Check if the first number is in the list but the next one is not
            if numbers[i] in list_set and numbers[i+1] not in list_set:
                failed_double_counts[list_name] += 1

    return failed_double_counts

def failed_consecutive_triples(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number']
    failed_triple_counts = {name: 0 for name in lists.keys()}

    for list_name, list_numbers in lists.items():
        list_set = set(list_numbers)
        for i in range(len(numbers) - 2):
            # Check various conditions where two out of three consecutive numbers are in the list but one is not
            if (numbers[i] in list_set and numbers[i+1] in list_set and numbers[i+2] not in list_set) or \
               (numbers[i] in list_set and numbers[i+1] not in list_set and numbers[i+2] in list_set) or \
               (numbers[i] not in list_set and numbers[i+1] in list_set and numbers[i+2] in list_set):
                failed_triple_counts[list_name] += 1

    return failed_triple_counts

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

            results, raw_numbers = analyze_and_extract_sequences(selected_file, selected_lists)
            st.subheader("Raw Sequence of Numbers:")
            st.write(raw_numbers)
            for list_name, stats in results.items():
                st.subheader(f"List: {list_name}")
                with st.expander("Show sequences"):
                    st.write("Sequences:", stats['sequences'])
                    

                with st.expander("Show actual sequences"):
                    st.write("actual_sequences:", stats['actual_sequences'])                    
                #st.write("Total series after first occurrence:", stats['total_series_after_first'])
                st.write("Average series length:", stats['average_series_length'])
                st.write("Consecutive Doubles:", stats['consecutive_doubles'])
                st.write("Failed Doubles:", stats['failed_doubles'])
                st.write("Consecutive Triples:", stats['consecutive_triples'])
                st.write("Failed Triples:", stats['failed_triples'])
                with st.expander("Full Analysis Details"):
                    st.write("Successful Double Sequences:")
                    for sequence in stats['double_sequences']:
                        st.write(sequence)

                    st.write("Failed Double Sequences:")
                    for sequence in stats['failed_double_sequences']:
                        st.write(sequence)

                    st.write("Successful Triple Sequences:")
                    for sequence in stats['triple_sequences']:
                        st.write(sequence)

                    st.write("Failed Triple Sequences:")
                    for sequence in stats['failed_triple_sequences']:
                        st.write(sequence)
                # Visualization of counts
                data = pd.DataFrame({
                    "Metric": ["Consecutive Doubles", "Failed Doubles", "Consecutive Triples", "Failed Triples"],
                    "Count": [stats['consecutive_doubles'], stats['failed_doubles'], stats['consecutive_triples'], stats['failed_triples']]
                })
                fig = px.bar(data, x='Metric', y='Count', title=f"Counts for {list_name}")
                st.plotly_chart(fig)

if __name__ == "__main__":
    app()
