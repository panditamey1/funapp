# funapp

This repository contains various Python applications. The `tk_roulette_app.py` script provides a simple Tkinter UI for logging roulette numbers.

## Running the roulette app

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Tkinter app:
   ```bash
   python tk_roulette_app.py
   ```

The app allows entering numbers (0-36) and stores each session in a new CSV
inside the `roulette_games` folder. Numbers are highlighted by color and you
can adjust the history box sizes from within the UI.

## Testing strategies

You can test betting strategies against saved CSV files using the strategy
builder:

```bash
python strategy_builder.py
```

Choose a CSV that contains a `Number` column, select the numbers or groups to
bet on, set the break condition and whether to use Martingale, then run the test
to see the simulated profit.
