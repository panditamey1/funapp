import streamlit as st

def calculate_martingale_rounds(initial_balance, risk, risk_to_reward, target):
    balance = initial_balance
    base_bet = risk
    rounds = 0
    steps = []

    while balance < target and balance >= base_bet:
        round_details = {
            "Round": rounds + 1,
            "Starting Balance": balance,
            "Bet Placed": base_bet
        }

        # Check if next bet can be placed
        if balance >= base_bet:
            balance -= base_bet  # Place the bet
            win = rounds % 2 == 0  # Simulating a loss every second round for simplicity
            if not win:
                # Loss: double the bet
                round_details["Outcome"] = "Loss"
                round_details["Ending Balance"] = balance
                base_bet *= 2
            else:
                # Win: reset bet and add winnings
                winnings = base_bet * risk_to_reward
                balance += winnings
                round_details["Outcome"] = "Win"
                round_details["Winnings"] = winnings
                round_details["Ending Balance"] = balance
                base_bet = risk

        steps.append(round_details)
        rounds += 1

    return steps, (rounds if balance >= target else -1)  # Return steps and rounds or -1 if bust

# Streamlit UI
st.title("Martingale Calculator")

initial_balance = st.number_input("Initial Balance", min_value=0.0, value=100.0, step=10.0)
risk = st.number_input("Risk per Play", min_value=0.0, value=10.0, step=0.01)
risk_to_reward = st.number_input("Risk to Reward Ratio", min_value=10.0, value=10.0, step=10.0)
target = st.number_input("Target Balance", min_value=0.0, value=200.0, step=1.0)

if st.button("Calculate"):
    steps, rounds = calculate_martingale_rounds(initial_balance, risk, risk_to_reward, target)
    if rounds == -1:
        st.write("Target not achievable with given balance and risk (bust likely).")
    else:
        st.write(f"Estimated number of plays needed: {rounds}")
        st.write("Detailed Steps:")
        for step in steps:
            st.write(step)

