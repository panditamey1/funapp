import pandas as pd
import streamlit as st

# Load the CSV file
#file_path = 'option-chain-ED-NIFTY-09-May-2024.csv'
st.title('Analysis')
strike_price = st.number_input('Enter Price', value=22460)
file_path = st.file_uploader('Upload CSV', type='csv')
if st.button('Load CSV'):
    
    data = pd.read_csv(file_path, skiprows=1)

    example_strike_price = strike_price

    def nearest_strikes(strike):
        base = (strike // 100) * 100  # Find the nearest lower multiple of 100
        return [base, base + 50, base + 100]
    # create new column ltp_mul_chng_in_oi for each strike
    # check chng in oi contains digits or not, if not then replace it with 0
    def check_digit(x):
        # check str is digit or not
        if x == '-':
            return 0
        else:
            return x
    def get_oi_changes_for_strikes(strike_prices):
        # Ensure 'STRIKE' is a float for proper comparison if not already converted
        if data['STRIKE'].dtype == object:
            data['STRIKE'] = data['STRIKE'].str.replace(',', '').astype(float)
        
        # Filter rows where the 'STRIKE' is in the list of given strike prices
        result = data[data['STRIKE'].isin(strike_prices)][['STRIKE', 'OI', 'CHNG IN OI', 'CHNG IN OI.1', 'OI.1', 'LTP', 'LTP.1']]
        
        return result


    data['OI'] = data['OI'].str.replace(',', '')
    data['CHNG IN OI'] = data['CHNG IN OI'].str.replace(',', '')
    data['OI.1'] = data['OI.1'].str.replace(',', '')
    data['CHNG IN OI.1'] = data['CHNG IN OI.1'].str.replace(',', '')
    data['LTP'] = data['LTP'].str.replace(',', '')
    data['LTP.1'] = data['LTP.1'].str.replace(',', '')

    data['CHNG IN OI'] = data['CHNG IN OI'].apply(check_digit).astype(float)
    data['CHNG IN OI.1'] = data['CHNG IN OI.1'].apply(check_digit).astype(float)
    data['OI'] = data['OI'].apply(check_digit).astype(float)
    data['OI.1'] = data['OI.1'].apply(check_digit).astype(float)
    data['LTP'] = data['LTP'].apply(check_digit).astype(float)
    data['LTP.1'] = data['LTP.1'].apply(check_digit).astype(float)
    nearest_strikes_list = nearest_strikes(example_strike_price)
    strike_data = get_oi_changes_for_strikes(nearest_strikes_list)
    print(strike_data)
    #      STRIKE        OI CHNG IN OI CHNG IN OI.1      OI.1
    # 43  22400.0    60,501     44,416       25,423    96,293
    # 44  22450.0    33,089     30,425       31,066    49,777
    # 45  22500.0  1,61,843   1,29,549       35,465  1,45,976

    # get sum of OI and CHNG IN OI for each strike



    data['call_ltp_mul_chng_in_oi'] = data['LTP'] * data['CHNG IN OI']
    data['put_ltp_mul_chng_in_oi'] = data['LTP.1'] * data['CHNG IN OI.1']

    # sum call ltp mul chng in oi and put ltp mul chng in oi
    sum_call_ltp_mul_chng_in_oi = data['call_ltp_mul_chng_in_oi'].sum()
    sum_put_ltp_mul_chng_in_oi = data['put_ltp_mul_chng_in_oi'].sum()
    strike_data['CHNG IN OI'] = strike_data['CHNG IN OI'].apply(check_digit)
    strike_data['CHNG IN OI.1'] = strike_data['CHNG IN OI.1'].apply(check_digit)
    #data.to_csv('strike_data.csv')

    sum_oi = strike_data['OI'].sum()
    sum_change_oi = strike_data['CHNG IN OI'].sum()
    sum_oi1 = strike_data['OI.1'].sum()
    sum_change_oi1 = strike_data['CHNG IN OI.1'].sum()

    total_call_oi = sum_oi + sum_change_oi
    total_put_oi = sum_oi1 + sum_change_oi1

    difference = total_call_oi - total_put_oi
    with st.expander("First strategy") :
        print(f'Total Call OI: {total_call_oi}')
        print(f'Total Put OI: {total_put_oi}')
        print(f'Difference: {difference}')
        st.write(f'Total C O: {total_call_oi}')
        st.write(f'Total P O: {total_put_oi}')
        st.write(f'Difference: {difference}')

        # ratio of call to put
        if total_call_oi > total_put_oi:
            ratio = total_call_oi / total_put_oi
        else:
            ratio = total_put_oi / total_call_oi
        if ratio < 225:
            print('Ratio is less than 225')
            st.write('Ratio is less than 225')
            if difference > 0:
                print('Bearish')
                print("Buy strike price: ", nearest_strikes_list[2])
                st.write('Bear')
                st.write(f'price: {nearest_strikes_list[2]}')
            else:
                print('Bullish')
                print("Buy strike price: ", nearest_strikes_list[0])
                st.write('Bull')
                st.write(f'price: {nearest_strikes_list[0]}')
        print("-----------------------------------------------------------------")
    st.write("-----------------------------------------------------------------")
    print("Second strategy")
    with st.expander("Second strategy") :
        # get sum ratio
        if sum_call_ltp_mul_chng_in_oi > sum_put_ltp_mul_chng_in_oi:
            ratio = sum_call_ltp_mul_chng_in_oi / sum_put_ltp_mul_chng_in_oi
        else:
            ratio = sum_put_ltp_mul_chng_in_oi / sum_call_ltp_mul_chng_in_oi

        print(f'call ltp mul chng in oi: {sum_call_ltp_mul_chng_in_oi}')
        print(f'put ltp mul chng in oi: {sum_put_ltp_mul_chng_in_oi}')
        print(f'Ratio: {ratio}')
        st.write(f'cl ltp mul chng in: {sum_call_ltp_mul_chng_in_oi}')
        st.write(f'pt ltp mul chng in: {sum_put_ltp_mul_chng_in_oi}')
        if ratio < 225:
            print('Ratio is less than 225')
            st.write('Ratio is less than 225')
            if sum_call_ltp_mul_chng_in_oi > sum_put_ltp_mul_chng_in_oi:
                print('Bearish')
                print("Buy strike price: ", nearest_strikes_list[2])
                st.write('Bear')
                st.write(f'price 1: {nearest_strikes_list[2]}')
                st.write(f'price 2: {nearest_strikes_list[2] + 100}')
            else:
                print('Bullish')
                print("Buy strike price: ", nearest_strikes_list[0])
                st.write('Bull')
                st.write(f'price 1: {nearest_strikes_list[0]}')
                st.write(f'price 2: {nearest_strikes_list[0] - 100}')
