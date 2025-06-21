import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
VOISINS = {22,18,29,7,28,12,35,3,26,0,32,15,19,4,21,2,25}
ORPHELINS = {1,20,14,31,9,17,34,6}
TIERS = {27,13,36,11,30,8,23,10,5,24,16,33}

class StrategyBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Roulette Strategy Tester')
        self.file_path = tk.StringVar()
        self.break_n = tk.IntVar(value=3)
        self.use_martingale = tk.BooleanVar(value=True)
        self.num_vars = []
        self.red_var = tk.BooleanVar()
        self.black_var = tk.BooleanVar()
        self.voisins_var = tk.BooleanVar()
        self.orphelins_var = tk.BooleanVar()
        self.tiers_var = tk.BooleanVar()
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
            ttk.Checkbutton(num_frame, text=str(n), variable=var).grid(row=n//12, column=n%12, sticky='w')

        opt_frame = ttk.Frame(self)
        opt_frame.pack(pady=5)
        ttk.Label(opt_frame, text='Break after').grid(row=0, column=0)
        ttk.Entry(opt_frame, textvariable=self.break_n, width=5).grid(row=0, column=1)
        ttk.Label(opt_frame, text='missing rounds').grid(row=0, column=2)
        ttk.Checkbutton(opt_frame, text='Use Martingale', variable=self.use_martingale).grid(row=0, column=3, padx=10)

        ttk.Button(self, text='Run Test', command=self.run_test).pack(pady=5)
        self.result_text = tk.Text(self, height=10, width=80, state='disabled')
        self.result_text.pack(padx=5, pady=5)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')])
        if path:
            self.file_path.set(path)

    def gather_selection(self):
        numbers = set()
        if self.red_var.get():
            numbers.update(RED_NUMBERS)
        if self.black_var.get():
            numbers.update(BLACK_NUMBERS)
        if self.voisins_var.get():
            numbers.update(VOISINS)
        if self.orphelins_var.get():
            numbers.update(ORPHELINS)
        if self.tiers_var.get():
            numbers.update(TIERS)
        for n, var in enumerate(self.num_vars):
            if var.get():
                numbers.add(n)
        return numbers

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
        selection = self.gather_selection()
        if not selection:
            messagebox.showerror('Error', 'Please select at least one number or group')
            return
        profit = self.simulate(numbers, selection, self.break_n.get(), self.use_martingale.get())
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f'Total profit: {profit}\n')
        self.result_text.config(state='disabled')

    @staticmethod
    def simulate(spins, selection, break_n, martingale):
        profit = 0
        gap = 0
        bet = 1
        betting = False
        for num in spins:
            if betting:
                if num in selection:
                    profit += bet
                    bet = 1
                    betting = False
                    gap = 0
                else:
                    profit -= bet
                    if martingale:
                        bet *= 2
            else:
                if num in selection:
                    gap = 0
                else:
                    gap += 1
                    if gap >= break_n:
                        betting = True
                        bet = 1
        return profit


def main():
    app = StrategyBuilder()
    app.mainloop()


if __name__ == '__main__':
    main()
