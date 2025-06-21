import streamlit as st
import pandas as pd
import os

CSV_PATH = 'roulette_history.csv'

RED_NUMBERS = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
BLACK_NUMBERS = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

VOISINS = [22,18,29,7,28,12,35,3,26,0,32,15,19,4,21,2,25]
ORPHELINS = [1,20,14,31,9,17,34,6]
TIERS = [27,13,36,11,30,8,23,10,5,24,16,33]

# ensure csv exists
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=['Number']).to_csv(CSV_PATH, index=False)

def load_numbers():
    return pd.read_csv(CSV_PATH)['Number'].tolist()

def save_number(num):
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame({'Number':[num]})], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

def undo_last():
    df = pd.read_csv(CSV_PATH)
    if not df.empty:
        df = df[:-1]
        df.to_csv(CSV_PATH, index=False)

def color_number(num):
    if num == 0:
        color = 'green'
    elif num in RED_NUMBERS:
        color = 'red'
    else:
        color = 'black'
    return f"<span style='color:{color}; font-weight:bold'>{num}</span>"

def sector_color(num):
    if num in VOISINS:
        color = 'green'
    elif num in ORPHELINS:
        color = 'blue'
    else:
        color = 'orange'
    return f"<span style='color:{color}; font-weight:bold'>{num}</span>"

def display_history(numbers, color_func, per_row=None):
    numbers = numbers[::-1]  # last to first
    if per_row:
        rows = []
        for i in range(0, len(numbers), per_row):
            row = ' '.join(color_func(n) for n in numbers[i:i+per_row])
            rows.append(row)
        return '<br>'.join(rows)
    else:
        return ' '.join(color_func(n) for n in numbers)

def dozen_count(numbers, start, end):
    return sum(1 for n in numbers if start <= n <= end)

def main():
    st.title('Roulette Number Logger')

    numbers = load_numbers()

    # Dozen metrics
    col1, col2, col3 = st.columns(3)
    col1.metric('Dozen 1', dozen_count(numbers,1,12))
    col2.metric('Dozen 2', dozen_count(numbers,13,24))
    col3.metric('Dozen 3', dozen_count(numbers,25,36))

    # Undo option
    if st.button('Undo Last Entry'):
        undo_last()
        st.experimental_rerun()

    st.write('---')
    st.subheader('Enter Number (0-36)')
    for start in range(0, 37, 12):
        cols = st.columns(min(12, 37-start))
        for i, col in enumerate(cols):
            num = start + i
            if num > 36:
                break
            if col.button(str(num), key=f'num_{num}'):
                save_number(num)
                st.experimental_rerun()

    st.write('---')
    st.subheader('History (Last to First)')
    st.markdown(display_history(numbers, color_number), unsafe_allow_html=True)

    st.write('---')
    st.subheader('History by Roulette Sections (20 per row)')
    st.markdown(display_history(numbers, sector_color, 20), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
