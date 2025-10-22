import tkinter as tk
import random
import pygame
import os

# ---------------- GAME SETTINGS ----------------
MAX_LINES = 3
MAX_BET = 10000
MIN_BET = 1
ROWS = 3
COLS = 3
SPIN_DELAY = 120  # milliseconds between spins

symbols = ["🍒", "🍋", "🔔", "💎", "🍀"]
symbol_weights = {"🍒": 2, "🍋": 4, "🔔": 6, "💎": 3, "🍀": 5}
symbol_values = {"🍒": 5, "🍋": 4, "🔔": 3, "💎": 6, "🍀": 2}


# ---------------- SOUND SETUP ----------------
pygame.mixer.init()
try:
    spin_sound = pygame.mixer.Sound("spin.wav")
    win_sound = pygame.mixer.Sound("win.wav")
except Exception:
    spin_sound = None
    win_sound = None


def play_sound(sound):
    if sound:
        try:
            sound.play()
        except:
            pass


# ---------------- GAME LOGIC ----------------
def get_slot_spin(rows, cols, symbol_weights):
    all_symbols = []
    for sym, count in symbol_weights.items():
        all_symbols.extend([sym] * count)
    return [[random.choice(all_symbols) for _ in range(rows)] for _ in range(cols)]


def check_winnings(columns, lines, bet, symbol_values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        sym = columns[0][line]
        if all(columns[c][line] == sym for c in range(COLS)):
            winnings += symbol_values[sym] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines


# ---------------- GUI ----------------
class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Lucky Slots Deluxe")
        self.root.state("zoomed")
        self.root.configure(bg="#111")

        self.balance = 0
        self.jackpot = 500

        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#111")
        self.main_frame.pack(expand=True, fill="both")

        # Jackpot display
        self.jackpot_label = tk.Label(self.main_frame, text=f"💎 Jackpot: £{self.jackpot}",
                                      font=("Arial", 26, "bold"), fg="#FFD700", bg="#111")
        self.jackpot_label.pack(pady=10)

        # Reels
        reels_frame = tk.Frame(self.main_frame, bg="#111")
        reels_frame.pack(pady=40)
        self.reels = [[tk.Label(reels_frame, text="", font=("Arial", 80), bg="#222", fg="white", width=3)
                       for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.reels[r][c].grid(row=r, column=c, padx=40, pady=20)

        # Deposit section
        deposit_frame = tk.Frame(self.main_frame, bg="#111")
        deposit_frame.pack(pady=10)
        tk.Label(deposit_frame, text="Deposit: £", font=("Arial", 18), fg="white", bg="#111").grid(row=0, column=0)
        self.deposit_entry = tk.Entry(deposit_frame, width=8, font=("Arial", 18))
        self.deposit_entry.grid(row=0, column=1, padx=5)
        tk.Button(deposit_frame, text="Add", command=self.deposit,
                  font=("Arial", 16), bg="#4CAF50", fg="black", width=6).grid(row=0, column=2, padx=5)

        # Controls
        control_frame = tk.Frame(self.main_frame, bg="#111")
        control_frame.pack(pady=10)
        tk.Label(control_frame, text="Bet per line:", font=("Arial", 16), fg="white", bg="#111").grid(row=0, column=0)
        self.bet_entry = tk.Entry(control_frame, width=5, font=("Arial", 16))
        self.bet_entry.insert(0, "10")
        self.bet_entry.grid(row=0, column=1, padx=10)
        tk.Label(control_frame, text="Lines:", font=("Arial", 16), fg="white", bg="#111").grid(row=0, column=2)
        self.lines_entry = tk.Entry(control_frame, width=5, font=("Arial", 16))
        self.lines_entry.insert(0, "3")
        self.lines_entry.grid(row=0, column=3, padx=10)

        # Balance and messages
        self.balance_label = tk.Label(self.main_frame, text=f"Balance: £{self.balance}",
                                      font=("Arial", 20), fg="#00FFAA", bg="#111")
        self.balance_label.pack(pady=10)
        self.message_label = tk.Label(self.main_frame, text="", font=("Arial", 18), fg="white", bg="#111")
        self.message_label.pack(pady=10)

        # Spin button
        self.spin_button = tk.Button(self.main_frame, text="🎯 SPIN", command=self.start_spin,
                                     font=("Arial", 28, "bold"), bg="#4CAF50", fg="gold", width=10, height=1)
        self.spin_button.pack(pady=20)

        # Quit button
        tk.Button(self.main_frame, text="💰 Cash Out / Quit", command=self.root.destroy,
                  font=("Arial", 14), bg="#E53935", fg="white", width=20).pack(pady=10)

        # Hover animation
        self.spin_button.bind("<Enter>", lambda e: e.widget.config(bg="#66BB6A"))
        self.spin_button.bind("<Leave>", lambda e: e.widget.config(bg="#4CAF50"))

    # Deposit money
    def deposit(self):
        amount_str = self.deposit_entry.get()
        if not amount_str.isdigit():
            self.message_label.config(text="Please enter a valid number!")
            return
        amount = int(amount_str)
        if amount <= 0:
            self.message_label.config(text="Deposit must be more than £0!")
            return
        self.balance += amount
        self.balance_label.config(text=f"Balance: £{self.balance}")
        self.deposit_entry.delete(0, tk.END)
        self.message_label.config(text=f"Deposited £{amount} successfully!")

    # Start spin
    def start_spin(self):
        if self.balance <= 0:
            self.message_label.config(text="Please deposit money first!")
            return
        try:
            self.bet = int(self.bet_entry.get())
            self.lines = int(self.lines_entry.get())
        except ValueError:
            self.message_label.config(text="Enter valid numbers!")
            return

        total_bet = self.bet * self.lines
        if self.bet < MIN_BET or self.bet > MAX_BET:
            self.message_label.config(text=f"Bet must be £{MIN_BET}-{MAX_BET}")
            return
        if self.lines < 1 or self.lines > MAX_LINES:
            self.message_label.config(text=f"Lines must be 1-{MAX_LINES}")
            return
        if total_bet > self.balance:
            self.message_label.config(text="Insufficient balance!")
            return

        self.balance -= total_bet
        self.balance_label.config(text=f"Balance: £{self.balance}")
        self.spin_button.config(state="disabled")
        self.message_label.config(text="🎡 Spinning...")
        self.current_step = 0
        play_sound(spin_sound)
        self.animate_spin()

    # Animate spin
    def animate_spin(self):
        if self.current_step < 10:
            for r in range(ROWS):
                for c in range(COLS):
                    self.reels[r][c].config(text=random.choice(symbols))
            self.current_step += 1
            self.root.after(SPIN_DELAY, self.animate_spin)
        else:
            self.show_result()

    # Show result
    def show_result(self):
        self.final_result = get_slot_spin(ROWS, COLS, symbol_weights)
        for r in range(ROWS):
            for c in range(COLS):
                self.reels[r][c].config(text=self.final_result[c][r], bg="#222")

        winnings, winning_lines = check_winnings(self.final_result, self.lines, self.bet, symbol_values)

        # Check jackpot (💎💎💎 middle line)
        middle_row = 1
        if all(self.final_result[c][middle_row] == "💎" for c in range(COLS)):
            winnings += self.jackpot
            self.message_label.config(text=f"💎 JACKPOT! You won £{self.jackpot}!!! 💎")
            self.jackpot = 500
        else:
            self.jackpot += 25  # grows each spin
            self.jackpot_label.config(text=f"💎 Jackpot: £{self.jackpot}")

        self.balance += winnings
        self.balance_label.config(text=f"Balance: £{self.balance}")

        if winnings > 0:
            play_sound(win_sound)
            self.flash_winning_lines(winning_lines)
            msg = f"🎉 You won £{winnings}!"
        else:
            msg = "No win this time."
        self.message_label.config(text=msg)
        self.spin_button.config(state="normal")

    # Flash winning lines
    def flash_winning_lines(self, winning_lines):
        for _ in range(4):
            for line in winning_lines:
                for c in range(COLS):
                    self.reels[line-1][c].config(bg="#FFD700")
            self.root.update()
            self.root.after(200)
            for line in winning_lines:
                for c in range(COLS):
                    self.reels[line-1][c].config(bg="#222")
            self.root.update()
            self.root.after(200)


# ---------------- RUN APP ----------------
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
