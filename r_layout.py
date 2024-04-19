import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def draw_roulette():
    # Create a circle for the roulette wheel
    fig, ax = plt.subplots()
    circle = plt.Circle((0.5, 0.5), 0.4, color='black', fill=False)
    ax.add_artist(circle)

    # Divide the circle into numbered segments
    for i in range(36):
        x = 0.5 + 0.4 * np.cos(np.radians(i * 10))
        y = 0.5 + 0.4 * np.sin(np.radians(i * 10))
        ax.plot([0.5, x], [0.5, y], 'k-')

        # Add numbers to the segments
        x_text = 0.5 + 0.45 * np.cos(np.radians(i * 10 + 5))
        y_text = 0.5 + 0.45 * np.sin(np.radians(i * 10 + 5))
        ax.text(x_text, y_text, str(i + 1), ha='center', va='center', color='red', fontsize=6, weight='bold')

    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

def main():
    st.title('Online Roulette Layout')
    
    # Draw roulette wheel
    fig = draw_roulette()
    st.pyplot(fig)

    # Spin button
    if st.button('Spin!'):
        st.write("Spinning the wheel...")  # This can be replaced with the actual spinning logic

if __name__ == '__main__':
    main()
