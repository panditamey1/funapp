import streamlit as st

def martingale_strategy(balance, risk, risk_to_reward, target):
    """
    Calculates the Martingale strategy based on the given parameters.

    Parameters:
    balance (float): The initial balance.
    risk (float): The risk percentage per bet.
    risk_to_reward (float): The risk-to-reward ratio.
    target (float): The target profit.

    Returns:
    list: The list of intermediate results, including the current balance, profit, and total bets.
    """
    profit = 0
    bet = balance * risk
    total_bets = 0
    results = []

    while profit < target:
        if bet > balance:
            return ["Insufficient balance to continue the Martingale strategy."]

        balance -= bet
        if risk_to_reward > 1:
            profit += bet * risk_to_reward
        else:
            profit -= bet

        bet *= 2
        total_bets += 1
        results.append((balance, profit, total_bets))

    return results

def main():
    st.title("Martingale Strategy Calculator")

    balance = st.number_input("Enter your initial balance:", min_value=1.0, step=0.01)
    risk = st.number_input("Enter the risk percentage per bet (e.g., 0.01 for 1%):", min_value=0.01, max_value=1.0, step=0.01)
    risk_to_reward = st.number_input("Enter the risk-to-reward ratio:", min_value=0.01, max_value=10.0, step=0.01)
    target = st.number_input("Enter the target profit:", min_value=0.01, step=0.01)

    if st.button("Calculate"):
        results = martingale_strategy(balance, risk, risk_to_reward, target)
        if isinstance(results[0], str):
            st.write(results[0])
        else:
            st.write("Intermediate Results:")
            for balance, profit, total_bets in results:
                st.write(f"Balance: {balance:.2f}, Profit: {profit:.2f}, Total Bets: {total_bets}")

if __name__ == "__main__":
    main()
