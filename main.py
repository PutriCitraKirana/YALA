import os
import requests
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

AUTH_FILE = 'auth.txt'
BANNER_URL = 'https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/yala.json'
CLAIM_URL = 'https://api-testnet.yala.org/api/points/dailyCollector'
POINTS_URL = 'https://api-testnet.yala.org/api/points/myPoints?chain=11155111'

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display banner from remote URL
def display_banner():
    try:
        response = requests.get(BANNER_URL)
        print(Fore.LIGHTGREEN_EX + response.text)
    except Exception:
        print(Fore.LIGHTCYAN_EX + 'Welcome to Yala Claim Script!')

# Read accounts from file
def read_auth_file():
    if not os.path.exists(AUTH_FILE):
        return []
    with open(AUTH_FILE, 'r') as file:
        data = file.read().strip()
    return [dict(zip(["name", "token"], line.split('|'))) for line in data.split('\n')]

# Write new account to file
def write_auth_file(name, token):
    with open(AUTH_FILE, 'a') as file:
        file.write(f"{name}|{token}\n")
    print(Fore.LIGHTGREEN_EX + f"Account {name} added successfully!")

# Claim daily points
def claim_daily_points(account):
    try:
        headers = {
            'Authorization': f"Bearer {account['token']}",
            'Accept': '*/*'
        }

        response = requests.post(CLAIM_URL, headers=headers)
        print(Fore.LIGHTGREEN_EX + f"[Success] Daily check-in for {account['name']}.")

        # Fetch balance and rank
        points_response = requests.get(POINTS_URL, headers=headers)
        points_data = points_response.json()

        print(Fore.LIGHTYELLOW_EX + f"\nBerries Balance: {points_data['data']['totalPoints']}")
        print(Fore.LIGHTBLUE_EX + f"Rank: {points_data['data']['rank']}")
    except Exception as error:
        print(Fore.LIGHTRED_EX + f"[Error] Failed to claim for {account['name']}: {error}")

# Show main menu
def show_menu():
    while True:
        print(Fore.LIGHTCYAN_EX + '\n1. Add Account')
        print('2. Run Once')
        print('3. Claim Every 24h')
        print('4. Exit')

        choice = input(Fore.LIGHTMAGENTA_EX + 'Select an option: ')
        clear_screen()

        if choice == '1':
            name = input(Fore.LIGHTYELLOW_EX + 'Enter account name: ')
            token = input(Fore.LIGHTYELLOW_EX + 'Enter auth token: ')
            write_auth_file(name, token)

        elif choice == '2':
            accounts = read_auth_file()
            for account in accounts:
                claim_daily_points(account)

        elif choice == '3':
            print(Fore.LIGHTBLUE_EX + "Starting 24-hour scheduler... Press Ctrl+C to stop.")
            while True:
                accounts = read_auth_file()
                for account in accounts:
                    claim_daily_points(account)
                time.sleep(24 * 60 * 60)

        elif choice == '4':
            print(Fore.LIGHTRED_EX + 'Exiting...')
            break

        else:
            print(Fore.LIGHTRED_EX + 'Invalid option. Try again.')

if __name__ == '__main__':
    clear_screen()
    display_banner()
    show_menu()
