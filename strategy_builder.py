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

def num_color(n: int) -> str:
    if n == 0:
        return 'green'
    return 'red' if n in RED_NUMBERS else 'black'

class StrategyBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Roulette Strategy Tester')
        self.file_path = tk.StringVar()
        self.break_n = tk.IntVar(value=3)
        self.use_martingale = tk.BooleanVar(value=True)
        self.first_bet = tk.DoubleVar(value=1.0)
        self.num_bet = tk.DoubleVar(value=1.0)
        self.red_bet = tk.DoubleVar(value=1.0)
        self.black_bet = tk.DoubleVar(value=1.0)
        self.voisins_bet = tk.DoubleVar(value=1.0)
        self.orphelins_bet = tk.DoubleVar(value=1.0)
        self.tiers_bet = tk.DoubleVar(value=1.0)
        self.split_bet = tk.DoubleVar(value=1.0)
        self.corner_bet = tk.DoubleVar(value=1.0)

        self.num_vars = []
        self.red_var = tk.BooleanVar()
        self.black_var = tk.BooleanVar()
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
        ttk.Checkbutton(sel_frame, text='Voisins du Zero', variable=self.voisins_var).grid(row=1, column=0, sticky='w')
        ttk.Checkbutton(sel_frame, text='Orphelins', variable=self.orphelins_var).grid(row=1, column=1, sticky='w')
        ttk.Checkbutton(sel_frame, text='Tiers du Cylindre', variable=self.tiers_var).grid(row=1, column=2, sticky='w')

        num_frame = ttk.Frame(sel_frame)
        num_frame.grid(row=2, column=0, columnspan=3, pady=5)
        for n in range(37):
            var = tk.BooleanVar()
            self.num_vars.append(var)
            color = num_color(n)
            cb = tk.Checkbutton(num_frame, text=str(n), variable=var,
                                fg='white', bg=color, selectcolor=color)
            cb.grid(row=n//12, column=n%12, sticky='w')

        bet_frame = ttk.LabelFrame(self, text='Bet Amounts')
        bet_frame.pack(fill='x', pady=5)
        labels = ['Singles', 'Red', 'Black', 'Voisins', 'Orphelins',
                  'Tiers', 'Splits', 'Corners']
        vars_ = [self.num_bet, self.red_bet, self.black_bet,
                 self.voisins_bet, self.orphelins_bet,
                 self.tiers_bet, self.split_bet, self.corner_bet]
        for i, (lab, var) in enumerate(zip(labels, vars_)):
            ttk.Label(bet_frame, text=lab).grid(row=0, column=2*i, padx=2)
            ttk.Entry(bet_frame, textvariable=var, width=5).grid(row=0, column=2*i+1)
        ttk.Label(bet_frame, text='Splits ex: 1-2,3-4').grid(row=1, column=0, columnspan=4, sticky='w')
        ttk.Entry(bet_frame, textvariable=self.split_entry, width=25).grid(row=1, column=4, columnspan=4, sticky='w')
        ttk.Label(bet_frame, text='Corners ex: 1-2-4-5').grid(row=2, column=0, columnspan=4, sticky='w')
        ttk.Entry(bet_frame, textvariable=self.corner_entry, width=25).grid(row=2, column=4, columnspan=4, sticky='w')


        opt_frame = ttk.Frame(self)
        opt_frame.pack(pady=5)
        ttk.Label(opt_frame, text='Break after').grid(row=0, column=0)
        ttk.Entry(opt_frame, textvariable=self.break_n, width=5).grid(row=0, column=1)
        ttk.Label(opt_frame, text='missing rounds').grid(row=0, column=2)
        ttk.Checkbutton(opt_frame, text='Use Martingale', variable=self.use_martingale).grid(row=0, column=3, padx=10)
        ttk.Label(opt_frame, text='First Bet').grid(row=0, column=4, padx=(10,0))
        ttk.Entry(opt_frame, textvariable=self.first_bet, width=7).grid(row=0, column=5)

        ttk.Button(self, text='Run Test', command=self.run_test).pack(pady=5)
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
        bets = []
        nums = {n for n, var in enumerate(self.num_vars) if var.get()}
        if nums:
            bets.append({'nums': nums, 'bet': self.num_bet.get()})
        if self.red_var.get():
            bets.append({'nums': RED_NUMBERS, 'bet': self.red_bet.get()})
        if self.black_var.get():
            bets.append({'nums': BLACK_NUMBERS, 'bet': self.black_bet.get()})
        if self.voisins_var.get():
            bets.append({'nums': VOISINS, 'bet': self.voisins_bet.get()})
        if self.orphelins_var.get():
            bets.append({'nums': ORPHELINS, 'bet': self.orphelins_bet.get()})
        if self.tiers_var.get():
            bets.append({'nums': TIERS, 'bet': self.tiers_bet.get()})
        for pair in self.parse_pairs(self.split_entry.get(), 2):
            bets.append({'nums': pair, 'bet': self.split_bet.get()})
        for quad in self.parse_pairs(self.corner_entry.get(), 4):
            bets.append({'nums': quad, 'bet': self.corner_bet.get()})
        return bets

    def estimate_total_bet_amount(self) -> float:
        """Estimate the starting bet amount given the selected options."""
        total = 0.0
        nums = [n for n, var in enumerate(self.num_vars) if var.get()]
        total += len(nums) * self.num_bet.get()
        total += len(self.parse_pairs(self.split_entry.get(), 2)) * self.split_bet.get()
        total += len(self.parse_pairs(self.corner_entry.get(), 4)) * self.corner_bet.get()
        if self.red_var.get():
            total += self.red_bet.get()
        if self.black_var.get():
            total += self.black_bet.get()
        if self.voisins_var.get():
            total += 9 * self.voisins_bet.get()
        if self.orphelins_var.get():
            total += 5 * self.orphelins_bet.get()
        if self.tiers_var.get():
            total += 6 * self.tiers_bet.get()
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
            numbers, bets, self.break_n.get(), self.use_martingale.get())
        hits = sum(1 for n in numbers if any(n in b['nums'] for b in bets))

        rate = hits / len(numbers) * 100 if numbers else 0
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(
            tk.END,
            f'Total profit: {profit}\nHits: {hits}/{len(numbers)} ({rate:.2f}%)\n'
            f'Max profit: {max(history):.2f}\nMin profit: {min(history):.2f}\n'
            f'Estimated Starting Bet: {est_total:.2f}\n')
        self.result_text.config(state='disabled')

        self.show_graph(history)
        self.show_rounds(rounds_df)


    def show_graph(self, history):
        fig = plt.Figure(figsize=(6, 3))
        ax = fig.add_subplot(111)
        ax.plot(range(len(history)), history, marker='o')
        ax.set_xlabel('Round')
        ax.set_ylabel('Profit')
        ax.set_title('Profit per Round')

        top = tk.Toplevel(self)
        top.title('Profit Graph')
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

        for _, row in df.iterrows():
            values = [row[col] for col in columns]
            tree.insert('', 'end', values=values)

        def save_csv():
            path = filedialog.asksaveasfilename(
                defaultextension='.csv', filetypes=[('CSV', '*.csv')])
            if path:
                df.to_csv(path, index=False)

        ttk.Button(top, text='Save CSV', command=save_csv).pack(pady=5)


    @staticmethod
    def simulate(spins, bets, break_n, martingale):
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
        profit = 0
        history = [0]
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
