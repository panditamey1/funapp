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
def cross_list_follow_count(file_path, list_a, list_b, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number'].tolist()
    a_follows_b = 0
    b_follows_a = 0
    a_not_follows_b = 0
    b_not_follows_a = 0

    for i in range(len(numbers) - 1):
        if numbers[i] in lists[list_a] and numbers[i + 1] in lists[list_b]:
            a_follows_b += 1
        elif numbers[i] in lists[list_a] and numbers[i + 1] not in lists[list_b]:
            a_not_follows_b += 1
        
        if numbers[i] in lists[list_b] and numbers[i + 1] in lists[list_a]:
            b_follows_a += 1
        elif numbers[i] in lists[list_b] and numbers[i + 1] not in lists[list_a]:
            b_not_follows_a += 1

    return {
        f"{list_a} follows {list_b}": a_follows_b,
        f"{list_b} follows {list_a}": b_follows_a,
        f"{list_a} does not follow {list_b}": a_not_follows_b,
        f"{list_b} does not follow {list_a}": b_not_follows_a
    }
def save_lists(lists):
    with open(list_file_path, 'w') as file:
        json.dump(lists, file, indent=4)

def get_csv_files():
    """Returns a list of csv files from the csv_directory."""
    return glob.glob(os.path.join(csv_directory, '*.csv'))
def get_subsequences(predefined_list, numbers):
    subsequences = []
    in_sequence = False
    current_sequence = []

    for num in numbers:
        if num in predefined_list:
            if not in_sequence:
                if current_sequence:
                    subsequences.append(current_sequence)
                current_sequence = []
                in_sequence = True
            current_sequence.append(num)
        else:
            if in_sequence:
                current_sequence.append(num)
                subsequences.append(current_sequence)
                current_sequence = []
                in_sequence = False
            else:
                if current_sequence:
                    subsequences.append(current_sequence)
                    current_sequence = []

    # Append the last sequence if it ends at the last element
    if current_sequence:
        subsequences.append(current_sequence)

    return subsequences

def categorize_subsequences(subsequences, predefined_list):
    successful_doubles = []
    failed_doubles = []
    successful_triples = []
    failed_triples = []

    for seq in subsequences:
        if len(seq) >= 2:
            if seq[0] in predefined_list and seq[1] in predefined_list:
                successful_doubles.append(seq)
            else:
                failed_doubles.append(seq)
        if len(seq) >= 3:
            if seq[0] in predefined_list and seq[1] in predefined_list and seq[2] in predefined_list:
                successful_triples.append(seq)
            else:
                failed_triples.append(seq)

    return successful_doubles, failed_doubles, successful_triples, failed_triples

def analyze_and_extract_sequences(file_path, lists):
    df = pd.read_csv(file_path)
    numbers = df['Number'].tolist()
    
    stats = {name: {} for name in lists.keys()}

    for list_name, predefined_list in lists.items():
        subsequences = get_subsequences(predefined_list, numbers)
        
        # Unpack categorized sequences
        successful_doubles, failed_doubles, successful_triples, failed_triples = categorize_subsequences(subsequences, predefined_list)
        
        # Store results in stats dictionary
        stats[list_name]['successful_doubles'] = successful_doubles
        stats[list_name]['failed_doubles'] = failed_doubles
        stats[list_name]['successful_triples'] = successful_triples
        stats[list_name]['failed_triples'] = failed_triples
        stats[list_name]['total_doubles'] = len(successful_doubles) + len(failed_doubles)
        stats[list_name]['total_triples'] = len(successful_triples) + len(failed_triples)
        stats[list_name]['all_sequences'] = subsequences  # store all subsequences for further analysis if needed

    return stats, numbers







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
                    st.write("Sequences:", stats['all_sequences'])
                    
                st.write(f"Total Doubles: {stats['total_doubles']}")
                st.write(f"Total Triples: {stats['total_triples']}")
                st.write(f"Successful Doubles: {len(stats['successful_doubles'])}")
                st.write(f"Failed Doubles: {len(stats['failed_doubles'])}")
                st.write(f"Successful Triples: {len(stats['successful_triples'])}")
                st.write(f"Failed Triples: {len(stats['failed_triples'])}")
                # show above in table with percentages
                data = pd.DataFrame({
                    "Metric": ["% Successful Doubles", "% Failed Doubles", "% Successful Triples", "% Failed Triples"],
                    "Percentage": [len(stats['successful_doubles']) / stats['total_doubles'] * 100, len(stats['failed_doubles']) / stats['total_doubles'] * 100, len(stats['successful_triples']) / stats['total_triples'] * 100, len(stats['failed_triples']) / stats['total_triples'] * 100]
                })
                fig = px.bar(data, x='Metric', y='Percentage', title=f"Percentages for {list_name}")
                st.plotly_chart(fig)
                with st.expander("Show Successful Doubles"):
                    st.write(pd.DataFrame(stats['successful_doubles']))
                with st.expander("Show Failed Doubles"):
                    st.write(pd.DataFrame(stats['failed_doubles']))
                with st.expander("Show Successful Triples"):
                    st.write(pd.DataFrame(stats['successful_triples']))
                with st.expander("Show Failed Triples"):
                    st.write(pd.DataFrame(stats['failed_triples']))

                # Visualization of counts
                data = pd.DataFrame({
                    "Metric": ["Consecutive Doubles", "Failed Doubles", "Consecutive Triples", "Failed Triples"],
                    "Count": [len(stats['successful_doubles']), len(stats['failed_doubles']), len(stats['successful_triples']), len(stats['failed_triples'])]
                })
                fig = px.bar(data, x='Metric', y='Count', title=f"Counts for {list_name}")
                st.plotly_chart(fig)
            list_pairs = [("Big", "Small"), ("Big", "Orph"), ("Small", "Orph")]
            for pair in list_pairs:
                results = cross_list_follow_count(selected_file, pair[0], pair[1], lists)
                st.write(pair)
                for k, v in results.items():
                    st.write(f"{k}: {v}")
if __name__ == "__main__":
    app()
