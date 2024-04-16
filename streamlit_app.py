import streamlit as st
import pandas as pd
import os
import glob

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

def delete_last_number(file_path):
    """Deletes the last number added to the CSV."""
    df = pd.read_csv(file_path)
    if not df.empty:
        df = df[:-1]  # Remove the last row
        df.to_csv(file_path, index=False)

def app():
    st.title('Manage CSV Files and Input Numbers')

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

    # Display last 5 numbers and deletion option
    if selected_file:
        st.write(f'You are working with: {selected_file}')
        df = pd.read_csv(selected_file)
        if not df.empty:
            st.write('Last 5 numbers:', df['Number'].tail(5))
            if st.button('Delete Last Number'):
                delete_last_number(selected_file)
                st.success('Last number deleted successfully.')
        
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

    # File download link
    if selected_file:
        st.download_button('Download CSV', data=pd.read_csv(selected_file).to_csv(index=False), file_name=os.path.basename(selected_file), mime='text/csv')

# Run the app function to start Streamlit app
if __name__ == "__main__":
    app()
