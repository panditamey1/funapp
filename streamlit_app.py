import streamlit as st
import pandas as pd
import os

# Predefined list of numbers
numbers_list = [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25]

# File path for the CSV where numbers will be stored
file_path = 'numbers.csv'

# Initialize the CSV file if it does not exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['Number'])
    df.to_csv(file_path, index=False)

def save_number(num):
    # Load existing data
    df = pd.read_csv(file_path)
    # Create a new DataFrame for the new number
    new_row = pd.DataFrame({'Number': [num]})
    # Use concat to append the new row
    df = pd.concat([df, new_row], ignore_index=True)
    # Save back to CSV
    df.to_csv(file_path, index=False)

def analyze_number(num):
    # Load numbers from CSV
    df = pd.read_csv(file_path)
    # Count occurrences of the number in the predefined list
    count = df[df['Number'].isin([num])]['Number'].count()
    return count

def total_matches():
    # Load numbers from CSV
    df = pd.read_csv(file_path)
    # Count how many numbers in CSV are in the predefined list
    matches = df[df['Number'].isin(numbers_list)].shape[0]
    total = df.shape[0]
    return matches, total

# Streamlit user interface
st.title('Number Input and Analysis')

# Create buttons for numbers 0 to 36 and handle interactions
col1, col2 = st.columns(2)

with col1:
    for i in range(19):  # First 19 numbers
        if st.button(f'{i}', key=f'num_{i}'):
            save_number(i)
            count = analyze_number(i)
            matches, total = total_matches()
            st.success(f'Number {i} saved!')
            st.info(f'The number {i} has appeared {count} times in the list.')
            st.info(f'Out of {total} entries, {matches} are in the predefined list.')

with col2:
    for i in range(19, 37):  # Remaining numbers
        if st.button(f'{i}', key=f'num_{i}'):
            save_number(i)
            count = analyze_number(i)
            matches, total = total_matches()
            st.success(f'Number {i} saved!')
            st.info(f'The number {i} has appeared {count} times in the list.')
            st.info(f'Out of {total} entries, {matches} are in the predefined list.')
