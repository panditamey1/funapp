import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
VOISINS = {22,18,29,7,28,12,35,3,26,0,32,15,19,4,21,2,25}
ORPHELINS = {1,20,14,31,9,17,34,6}
TIERS = {27,13,36,11,30,8,23,10,5,24,16,33}

EVEN_NUMBERS = {n for n in range(1, 37) if n % 2 == 0}
ODD_NUMBERS = {n for n in range(1, 37) if n % 2 == 1}
LOW_NUMBERS = set(range(1, 19))
HIGH_NUMBERS = set(range(19, 37))
DOZEN_1 = set(range(1, 13))
DOZEN_2 = set(range(13, 25))
DOZEN_3 = set(range(25, 37))
COLUMN_1 = {n for n in range(1, 37) if (n - 1) % 3 == 0}
COLUMN_2 = {n for n in range(1, 37) if (n - 2) % 3 == 0}
COLUMN_3 = {n for n in range(1, 37) if (n - 3) % 3 == 0}


def roulette_bets_table(min_bet):
    bets = [
        {"Bet": "Red / Black", "units": 1, "Type": "Even Money"},
        {"Bet": "Even / Odd", "units": 1, "Type": "Even Money"},
        {"Bet": "Low / High", "units": 1, "Type": "Even Money"},
        {"Bet": "Dozen", "units": 1, "Type": "Dozen (2:1)"},
        {"Bet": "Column", "units": 1, "Type": "Column (2:1)"},
        {"Bet": "6 Number", "units": 1, "Type": "Line (5:1)"},
        {"Bet": "5 Number", "units": 1, "Type": "Top Line (6:1)"},
        {"Bet": "4 Number", "units": 1, "Type": "Corner (8:1)"},
        {"Bet": "3 Number", "units": 1, "Type": "Street (11:1)"},
        {"Bet": "2 Number", "units": 1, "Type": "Split (17:1)"},
        {"Bet": "Single Number", "units": 1, "Type": "Straight (35:1)"},
        {"Bet": "Voisins du Zero (0,2,3)", "units": 2, "Type": "Basket"},
        {"Bet": "Voisins du Zero (4,7)", "units": 1, "Type": "Split"},
        {"Bet": "Voisins du Zero (12,15)", "units": 1, "Type": "Split"},
        {"Bet": "Voisins du Zero (18,21)", "units": 1, "Type": "Split"},
        {"Bet": "Voisins du Zero (19,22)", "units": 1, "Type": "Split"},
        {"Bet": "Voisins du Zero (25,26,28,29)", "units": 2, "Type": "Corner"},
        {"Bet": "Voisins du Zero (32,35)", "units": 1, "Type": "Split"},
        {"Bet": "Jeu Zero (0,3)", "units": 1, "Type": "Split"},
        {"Bet": "Jeu Zero (12,15)", "units": 1, "Type": "Split"},
        {"Bet": "Jeu Zero (26)", "units": 1, "Type": "Straight"},
        {"Bet": "Jeu Zero (32,35)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (5,8)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (10,11)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (13,16)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (23,24)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (27,30)", "units": 1, "Type": "Split"},
        {"Bet": "Tiers du Cylindre (33,36)", "units": 1, "Type": "Split"},
        {"Bet": "Orphelins (1)", "units": 1, "Type": "Straight"},
        {"Bet": "Orphelins (6,9)", "units": 1, "Type": "Split"},
        {"Bet": "Orphelins (14,17)", "units": 1, "Type": "Split"},
        {"Bet": "Orphelins (17,20)", "units": 1, "Type": "Split"},
        {"Bet": "Orphelins (31,34)", "units": 1, "Type": "Split"},
        {"Bet": "Neighbours", "units": 5, "Type": "Neighbours (custom)"},
        {"Bet": "Final 0", "units": 4, "Type": "Finale"},
        {"Bet": "Final 1", "units": 4, "Type": "Finale"},
        {"Bet": "Final 2", "units": 4, "Type": "Finale"},
        {"Bet": "Final 3", "units": 4, "Type": "Finale"},
        {"Bet": "Final 4", "units": 4, "Type": "Finale"},
        {"Bet": "Final 5", "units": 4, "Type": "Finale"},
        {"Bet": "Final 6", "units": 4, "Type": "Finale"},
        {"Bet": "Final 7", "units": 3, "Type": "Finale"},
        {"Bet": "Final 8", "units": 3, "Type": "Finale"},
        {"Bet": "Final 9", "units": 3, "Type": "Finale"},
    ]

    for bet in bets:
        bet['Total Amount'] = bet['units'] * min_bet

    bet_summary = {bet["Bet"]: {
        "Units": bet["units"],
        "Total Amount": bet["Total Amount"],
        "Type": bet["Type"]
    } for bet in bets}

    return bet_summary

def num_color(n: int) -> str:
    if n == 0:
        return 'green'
    return 'red' if n in RED_NUMBERS else 'black'

def sector_color(n: int) -> str:
    """Return color based on roulette sector."""
    if n in VOISINS:
        return 'green'
    if n in ORPHELINS:
        return 'blue'
    return 'orange'

class StrategyBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Roulette Strategy Tester')
        self.file_path = tk.StringVar()
        self.break_n = tk.IntVar(value=3)
        self.use_martingale = tk.BooleanVar(value=True)
        self.initial_balance = tk.DoubleVar(value=100.0)
        self.min_bet = tk.IntVar(value=1)

        self.num_vars = []
        self.red_var = tk.BooleanVar()
        self.black_var = tk.BooleanVar()
        self.even_var = tk.BooleanVar()
        self.odd_var = tk.BooleanVar()
        self.low_var = tk.BooleanVar()
        self.high_var = tk.BooleanVar()
        self.dozen1_var = tk.BooleanVar()
        self.dozen2_var = tk.BooleanVar()
        self.dozen3_var = tk.BooleanVar()
        self.column1_var = tk.BooleanVar()
        self.column2_var = tk.BooleanVar()
        self.column3_var = tk.BooleanVar()
        self.voisins_var = tk.BooleanVar()
        self.orphelins_var = tk.BooleanVar()
        self.tiers_var = tk.BooleanVar()
        self.split_entry = tk.StringVar()
        self.corner_entry = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        file_frame = ttk.Frame(self)
        file_frame.pack(fill='x', pady=5)
        ttk.Label(file_frame, text='CSV File:').pack(side='left')
        ttk.Entry(file_frame, textvariable=self.file_path, width=40).pack(side='left', padx=5)
        ttk.Button(file_frame, text='Browse', command=self.browse_file).pack(side='left')

        sel_frame = ttk.LabelFrame(self, text='Select Numbers / Groups')
        sel_frame.pack(fill='x', pady=5)
        ttk.Checkbutton(sel_frame, text='Red', variable=self.red_var).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(sel_frame, text='Black', variable=self.black_var).grid(row=0, column=1, sticky='w')
        ttk.Checkbutton(sel_frame, text='Even', variable=self.even_var).grid(row=0, column=2, sticky='w')
        ttk.Checkbutton(sel_frame, text='Odd', variable=self.odd_var).grid(row=0, column=3, sticky='w')
        ttk.Checkbutton(sel_frame, text='Low (1-18)', variable=self.low_var).grid(row=1, column=0, sticky='w')
        ttk.Checkbutton(sel_frame, text='High (19-36)', variable=self.high_var).grid(row=1, column=1, sticky='w')
        ttk.Checkbutton(sel_frame, text='1st Dozen', variable=self.dozen1_var).grid(row=1, column=2, sticky='w')
        ttk.Checkbutton(sel_frame, text='2nd Dozen', variable=self.dozen2_var).grid(row=1, column=3, sticky='w')
        ttk.Checkbutton(sel_frame, text='3rd Dozen', variable=self.dozen3_var).grid(row=1, column=4, sticky='w')
        ttk.Checkbutton(sel_frame, text='Column 1', variable=self.column1_var).grid(row=2, column=0, sticky='w')
        ttk.Checkbutton(sel_frame, text='Column 2', variable=self.column2_var).grid(row=2, column=1, sticky='w')
        ttk.Checkbutton(sel_frame, text='Column 3', variable=self.column3_var).grid(row=2, column=2, sticky='w')
        ttk.Checkbutton(sel_frame, text='Voisins du Zero', variable=self.voisins_var).grid(row=2, column=3, sticky='w')
        ttk.Checkbutton(sel_frame, text='Orphelins', variable=self.orphelins_var).grid(row=2, column=4, sticky='w')
        ttk.Checkbutton(sel_frame, text='Tiers du Cylindre', variable=self.tiers_var).grid(row=2, column=5, sticky='w')

        num_frame = ttk.Frame(sel_frame)
        num_frame.grid(row=3, column=0, columnspan=6, pady=5)
        for n in range(37):
            var = tk.BooleanVar()
            self.num_vars.append(var)
            color = num_color(n)
            cb = tk.Checkbutton(num_frame, text=str(n), variable=var,
                                fg='white', bg=color, selectcolor=color)
            cb.grid(row=n//12, column=n%12, sticky='w')

        bet_frame = ttk.LabelFrame(self, text='Splits and Corners')
        bet_frame.pack(fill='x', pady=5)
        ttk.Label(bet_frame, text='Splits ex: 1-2,3-4').grid(row=0, column=0, columnspan=2, sticky='w')
        ttk.Entry(bet_frame, textvariable=self.split_entry, width=25).grid(row=0, column=2, columnspan=2, sticky='w')
        ttk.Label(bet_frame, text='Corners ex: 1-2-4-5').grid(row=1, column=0, columnspan=2, sticky='w')
        ttk.Entry(bet_frame, textvariable=self.corner_entry, width=25).grid(row=1, column=2, columnspan=2, sticky='w')


        opt_frame = ttk.Frame(self)
        opt_frame.pack(pady=5)
        ttk.Label(opt_frame, text='Break after').grid(row=0, column=0)
        ttk.Entry(opt_frame, textvariable=self.break_n, width=5).grid(row=0, column=1)
        ttk.Label(opt_frame, text='missing rounds').grid(row=0, column=2)
        ttk.Checkbutton(opt_frame, text='Use Martingale', variable=self.use_martingale).grid(row=0, column=3, padx=10)
        ttk.Label(opt_frame, text='Initial Balance').grid(row=0, column=4, padx=(10,0))
        ttk.Entry(opt_frame, textvariable=self.initial_balance, width=7).grid(row=0, column=5)
        ttk.Label(opt_frame, text='Min Bet').grid(row=0, column=6, padx=(10,0))
        ttk.Combobox(opt_frame, textvariable=self.min_bet, values=list(range(1,11)), width=5, state='readonly').grid(row=0, column=7)

        ttk.Button(self, text='Run Test', command=self.run_test).pack(pady=5)
        ttk.Button(self, text='Show Bet Table', command=self.show_bets_table).pack(pady=5)
        self.result_text = tk.Text(self, height=10, width=80, state='disabled')
        self.result_text.pack(padx=5, pady=5)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')])
        if path:
            self.file_path.set(path)

    def parse_pairs(self, text, count):
        pairs = []
        if not text:
            return pairs
        for item in text.replace(',', ' ').split():
            nums = item.split('-')
            if len(nums) != count:
                continue
            try:
                vals = [int(n) for n in nums]
            except ValueError:
                continue
            if all(0 <= n <= 36 for n in vals):
                pairs.append(set(vals))
        return pairs

    def gather_bets(self):
        bet_amt = self.min_bet.get()
        bets = []
        nums = {n for n, var in enumerate(self.num_vars) if var.get()}
        if nums:
            bets.append({'nums': nums, 'bet': bet_amt})
        if self.red_var.get():
            bets.append({'nums': RED_NUMBERS, 'bet': bet_amt})
        if self.black_var.get():
            bets.append({'nums': BLACK_NUMBERS, 'bet': bet_amt})
        if self.even_var.get():
            bets.append({'nums': EVEN_NUMBERS, 'bet': bet_amt})
        if self.odd_var.get():
            bets.append({'nums': ODD_NUMBERS, 'bet': bet_amt})
        if self.low_var.get():
            bets.append({'nums': LOW_NUMBERS, 'bet': bet_amt})
        if self.high_var.get():
            bets.append({'nums': HIGH_NUMBERS, 'bet': bet_amt})
        if self.dozen1_var.get():
            bets.append({'nums': DOZEN_1, 'bet': bet_amt})
        if self.dozen2_var.get():
            bets.append({'nums': DOZEN_2, 'bet': bet_amt})
        if self.dozen3_var.get():
            bets.append({'nums': DOZEN_3, 'bet': bet_amt})
        if self.column1_var.get():
            bets.append({'nums': COLUMN_1, 'bet': bet_amt})
        if self.column2_var.get():
            bets.append({'nums': COLUMN_2, 'bet': bet_amt})
        if self.column3_var.get():
            bets.append({'nums': COLUMN_3, 'bet': bet_amt})
        if self.voisins_var.get():
            bets.append({'nums': VOISINS, 'bet': bet_amt})
        if self.orphelins_var.get():
            bets.append({'nums': ORPHELINS, 'bet': bet_amt})
        if self.tiers_var.get():
            bets.append({'nums': TIERS, 'bet': bet_amt})
        for pair in self.parse_pairs(self.split_entry.get(), 2):
            bets.append({'nums': pair, 'bet': bet_amt})
        for quad in self.parse_pairs(self.corner_entry.get(), 4):
            bets.append({'nums': quad, 'bet': bet_amt})
        return bets

    def estimate_total_bet_amount(self) -> float:
        """Estimate the starting bet amount given the selected options."""
        bet = self.min_bet.get()
        total = 0.0
        table = roulette_bets_table(bet)

        nums = [n for n, var in enumerate(self.num_vars) if var.get()]
        total += len(nums) * bet
        total += len(self.parse_pairs(self.split_entry.get(), 2)) * bet
        total += len(self.parse_pairs(self.corner_entry.get(), 4)) * bet

        if self.red_var.get():
            total += table["Red / Black"]["Total Amount"]
        if self.black_var.get():
            total += table["Red / Black"]["Total Amount"]
        if self.even_var.get():
            total += table["Even / Odd"]["Total Amount"]
        if self.odd_var.get():
            total += table["Even / Odd"]["Total Amount"]
        if self.low_var.get():
            total += table["Low / High"]["Total Amount"]
        if self.high_var.get():
            total += table["Low / High"]["Total Amount"]
        if self.dozen1_var.get():
            total += table["Dozen"]["Total Amount"]
        if self.dozen2_var.get():
            total += table["Dozen"]["Total Amount"]
        if self.dozen3_var.get():
            total += table["Dozen"]["Total Amount"]
        if self.column1_var.get():
            total += table["Column"]["Total Amount"]
        if self.column2_var.get():
            total += table["Column"]["Total Amount"]
        if self.column3_var.get():
            total += table["Column"]["Total Amount"]
        if self.voisins_var.get():
            voisins_total = sum(v["Total Amount"] for k, v in table.items()
                                if k.startswith("Voisins du Zero"))
            total += voisins_total
        if self.orphelins_var.get():
            orphelins_total = sum(v["Total Amount"] for k, v in table.items()
                                   if k.startswith("Orphelins"))
            total += orphelins_total
        if self.tiers_var.get():
            tiers_total = sum(v["Total Amount"] for k, v in table.items()
                              if k.startswith("Tiers du Cylindre"))
            total += tiers_total

        return total


    def run_test(self):
        path = self.file_path.get()
        if not path:
            messagebox.showerror('Error', 'Please select a CSV file')
            return
        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to read CSV: {e}')
            return
        if 'Number' not in df.columns:
            messagebox.showerror('Error', 'CSV must have a Number column')
            return
        numbers = df['Number'].tolist()
        bets = self.gather_bets()
        if not bets:
            messagebox.showerror('Error', 'Please select at least one number or group')
            return
        est_total = self.estimate_total_bet_amount()
        profit, history, rounds_df = self.simulate(
            numbers, bets, self.break_n.get(),
            self.use_martingale.get(), self.initial_balance.get())

        hits = sum(1 for n in numbers if any(n in b['nums'] for b in bets))

        rate = hits / len(numbers) * 100 if numbers else 0
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(
            tk.END,
            f'Final Balance: {profit:.2f}\n'
            f'Profit/Loss: {profit - self.initial_balance.get():.2f}\n'
            f'Hits: {hits}/{len(numbers)} ({rate:.2f}%)\n'
            f'Max balance: {max(history):.2f}\nMin balance: {min(history):.2f}\n'


            f'Estimated Starting Bet: {est_total:.2f}\n')
        self.result_text.config(state='disabled')

        self.show_graph(history)
        self.show_rounds(rounds_df)


    def show_graph(self, history):
        fig = plt.Figure(figsize=(6, 3))
        ax = fig.add_subplot(111)
        ax.plot(range(len(history)), history, marker='o')
        ax.set_xlabel('Round')
        ax.set_ylabel('Balance')
        ax.set_title('Balance per Round')

        top = tk.Toplevel(self)
        top.title('Balance Graph')
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_rounds(self, df: pd.DataFrame):
        """Display dataframe of rounds in a scrollable tree view and allow saving."""
        top = tk.Toplevel(self)
        top.title('Rounds with Bets')

        frame = ttk.Frame(top)
        frame.pack(fill='both', expand=True)

        columns = list(df.columns)
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        tree.tag_configure('red', foreground='red')
        tree.tag_configure('black', foreground='black')
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('blue', foreground='blue')
        tree.tag_configure('orange', foreground='orange')
        tree.tag_configure('win', background='#ccffcc')
        tree.tag_configure('loss', background='#ffcccc')

        use_sectors = any([self.voisins_var.get(),
                           self.orphelins_var.get(),
                           self.tiers_var.get()])

        for _, row in df.iterrows():
            values = [row[col] for col in columns]
            if use_sectors:
                color_tag = sector_color(row['Number'])
            else:
                color_tag = num_color(row['Number'])
            change_tag = 'win' if row['WIN/LOSS'] >= 0 else 'loss'
            tree.insert('', 'end', values=values, tags=(color_tag, change_tag))


        def save_csv():
            path = filedialog.asksaveasfilename(
                defaultextension='.csv', filetypes=[('CSV', '*.csv')])
            if path:
                df.to_csv(path, index=False)

        ttk.Button(top, text='Save CSV', command=save_csv).pack(pady=5)

    def show_bets_table(self):
        """Display the full roulette bets table for the selected minimum bet."""
        table = roulette_bets_table(self.min_bet.get())

        top = tk.Toplevel(self)
        top.title('Roulette Bets Table')

        tree = ttk.Treeview(top, columns=('Bet', 'Units', 'Total', 'Type'), show='headings')
        for col in ('Bet', 'Units', 'Total', 'Type'):
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        for bet, vals in table.items():
            tree.insert('', 'end', values=(bet, vals['Units'], vals['Total Amount'], vals['Type']))
        tree.pack(fill='both', expand=True)


    @staticmethod
    def simulate(spins, bets, break_n, martingale, initial_balance=0):
        class BetState:
            def __init__(self, numbers, first):
                self.numbers = numbers
                self.first = first
                self.bet = first
                self.gap = 0
                self.betting = False

            def step(self, num):
                profit = 0
                if self.betting:
                    if num in self.numbers:
                        profit += self.bet
                        self.bet = self.first
                        self.betting = False
                        self.gap = 0
                    else:
                        profit -= self.bet
                        if martingale:
                            self.bet *= 2
                else:
                    if num in self.numbers:
                        self.gap = 0
                    else:
                        self.gap += 1
                        if self.gap >= break_n:
                            self.betting = True
                            self.bet = self.first
                return profit

        states = [BetState(b['nums'], b['bet']) for b in bets]
        profit = initial_balance
        history = [initial_balance]
        rounds = []
        total_profit = 0
        total_loss = 0
        for idx, num in enumerate(spins, start=1):
            bet_flag = any(state.betting for state in states)
            total_bet = sum(state.bet for state in states if state.betting)
            prev_profit = profit
            for state in states:
                profit += state.step(num)
            change = profit - prev_profit
            if change >= 0:
                total_profit += change
            else:
                total_loss += -change
            history.append(profit)
            rounds.append({
                'Round': idx,
                'Number': num,
                'Bet Placed?': bool(total_bet),
                'Amount': total_bet,
                'WIN/LOSS': change,
                'Total Balance': profit,
                'Total Profit': total_profit,
                'Total Loss': total_loss
            })
        df = pd.DataFrame(rounds)
        return profit, history, df



def main():
    app = StrategyBuilder()
    app.mainloop()


if __name__ == '__main__':
    main()
