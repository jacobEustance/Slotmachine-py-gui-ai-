import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {  #this is how you make a dictionary
    "🥎": 2,
    "🎱": 4,
    "⚽️": 6,
    "🏀": 8
}

symbol_value = {  #this is how you make a dictionary
    "🥎": 5,
    "🎱": 4,
    "⚽️": 3,
    "🏀": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_check = column[line]
            if symbol != symbol_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(lines + 1)

    return winnings, winning_lines

def get_slot_spin(rows, cols, symbols) :
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)
    
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end = " | ")
            else:
                print(column[row], end = "")

        print()

def deposit():


    while True:
        amount = input('what would you like to depostit? £')
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print('amount must be greater than £0')
        else:
            print('please enter a number!')
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print('Enter a valid number of lines')
        else:
            print('please enter a number!')
    return lines

def get_bet():
    while True:
        get_bet = input("Enter bet amount for each line: ")
        if get_bet.isdigit():
            get_bet = int(get_bet)
            if MIN_BET <= get_bet <= MAX_BET:
                break
            else:
                print(f'Enter a bet between £{MIN_BET} - £{MAX_BET}.')
        else:
            print('please enter a number!')
    return get_bet

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f'You dont have enough to bet that amount, your current balance is £{balance}')
        else:
            break
    print(f"you are betting £{bet} for {lines} lines. Total bet is equal to £{total_bet} ")

    slots = get_slot_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f'You won £{winnings}.')
    print(f'You won on lines:', *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"current balance is £{balance}")
        answer = input("press enter to play (q to quit)")
        if answer  == "q":
            break
        balance += spin(balance)
    print(f'You left with £{balance}')

main()