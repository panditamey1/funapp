import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk

CSV_DIR = 'roulette_games'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
CSV_PATH = os.path.join(CSV_DIR, f'game_{timestamp}.csv')

RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

VOISINS = {22,18,29,7,28,12,35,3,26,0,32,15,19,4,21,2,25}
ORPHELINS = {1,20,14,31,9,17,34,6}
TIERS = {27,13,36,11,30,8,23,10,5,24,16,33}


def ensure_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Number'])


def load_numbers():
    ensure_csv()
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        return [int(row['Number']) for row in reader]


def save_number(num):
    ensure_csv()
    with open(CSV_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([num])


def undo_last():
    ensure_csv()
    rows = load_numbers()
    if rows:
        rows = rows[:-1]
        with open(CSV_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Number'])
            for n in rows:
                writer.writerow([n])


def color_number(num):
    if num == 0:
        return 'green'
    return 'red' if num in RED_NUMBERS else 'black'


def sector_color(num):
    if num in VOISINS:
        return 'green'
    if num in ORPHELINS:
        return 'blue'
    return 'orange'


class RouletteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Roulette Number Logger')
        # use full screen
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.numbers = load_numbers()

        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # Dozen counts
        top = ttk.Frame(self)
        top.pack(pady=5)
        self.d1_var = tk.StringVar()
        self.d2_var = tk.StringVar()
        self.d3_var = tk.StringVar()
        ttk.Label(top, textvariable=self.d1_var, width=12).grid(row=0, column=0)
        ttk.Label(top, textvariable=self.d2_var, width=12).grid(row=0, column=1)
        ttk.Label(top, textvariable=self.d3_var, width=12).grid(row=0, column=2)

        # Number buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        for num in range(37):
            r, c = divmod(num, 12)
            btn = ttk.Button(btn_frame, text=str(num), width=4,
                             command=lambda n=num: self.add_number(n))
            btn.grid(row=r, column=c, padx=2, pady=2)

        undo_btn = ttk.Button(self, text='Undo Last', command=self.undo)
        undo_btn.pack(pady=5)

        # Text box size controls
        size_frame = ttk.Frame(self)
        size_frame.pack(pady=5)
        ttk.Label(size_frame, text='History WxH').grid(row=0, column=0)
        self.hist_w = tk.IntVar(value=80)
        self.hist_h = tk.IntVar(value=2)
        ttk.Entry(size_frame, textvariable=self.hist_w, width=5).grid(row=0, column=1)
        ttk.Entry(size_frame, textvariable=self.hist_h, width=5).grid(row=0, column=2)
        ttk.Label(size_frame, text='Sector WxH').grid(row=0, column=3, padx=(10,0))
        self.sec_w = tk.IntVar(value=80)
        self.sec_h = tk.IntVar(value=6)
        ttk.Entry(size_frame, textvariable=self.sec_w, width=5).grid(row=0, column=4)
        ttk.Entry(size_frame, textvariable=self.sec_h, width=5).grid(row=0, column=5)
        ttk.Button(size_frame, text='Apply Size', command=self.apply_size).grid(row=0, column=6, padx=5)

        # History display
        hist_label = ttk.Label(self, text='History (Last to First)')
        hist_label.pack()
        self.hist_text = tk.Text(self, height=2, width=80, state='disabled')
        self.hist_text.pack(fill='x')
        self.hist_text.tag_config('red', background='red', foreground='white')
        self.hist_text.tag_config('black', background='black', foreground='white')
        self.hist_text.tag_config('green', background='green', foreground='white')

        # Sector history display
        sector_label = ttk.Label(self, text='History by Roulette Sections (20 per row)')
        sector_label.pack()
        self.sector_text = tk.Text(self, height=6, width=80, state='disabled')
        self.sector_text.pack(fill='both', expand=True)
        self.sector_text.tag_config('green', background='green', foreground='white')
        self.sector_text.tag_config('blue', background='blue', foreground='white')
        self.sector_text.tag_config('orange', background='orange', foreground='white')

    def add_number(self, num):
        save_number(num)
        self.numbers.append(num)
        self.update_ui()

    def undo(self):
        undo_last()
        if self.numbers:
            self.numbers.pop()
        self.update_ui()

    def update_ui(self):
        d1 = sum(1 for n in self.numbers if 1 <= n <= 12)
        d2 = sum(1 for n in self.numbers if 13 <= n <= 24)
        d3 = sum(1 for n in self.numbers if 25 <= n <= 36)
        self.d1_var.set(f'Dozen 1: {d1}')
        self.d2_var.set(f'Dozen 2: {d2}')
        self.d3_var.set(f'Dozen 3: {d3}')

        self.show_history()
        self.show_sector_history()

    def show_history(self):
        self.hist_text.config(state='normal')
        self.hist_text.delete('1.0', tk.END)
        for num in reversed(self.numbers):
            color = color_number(num)
            self.hist_text.insert(tk.END, f'{num} ', color)
        self.hist_text.config(state='disabled')

    def show_sector_history(self):
        self.sector_text.config(state='normal')
        self.sector_text.delete('1.0', tk.END)
        for i, num in enumerate(reversed(self.numbers)):
            color = sector_color(num)
            self.sector_text.insert(tk.END, f'{num} ', color)
            if (i + 1) % 20 == 0:
                self.sector_text.insert(tk.END, '\n')
        self.sector_text.config(state='disabled')

    def apply_size(self):
        self.hist_text.config(width=self.hist_w.get(), height=self.hist_h.get())
        self.sector_text.config(width=self.sec_w.get(), height=self.sec_h.get())
        

def main():
    app = RouletteApp()
    app.mainloop()


if __name__ == '__main__':
    main()
