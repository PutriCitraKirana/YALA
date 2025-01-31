import os
import requests
import time
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

AUTH_FILE = "auth.txt"
BANNER_URL = "https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/yala.json"
CLAIM_URL = "https://api-testnet.yala.org/api/points/dailyCollector"
POINTS_URL = "https://api-testnet.yala.org/api/points/myPoints?chain=11155111"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Display banner from remote URL
def display_banner():
    try:
        response = requests.get(BANNER_URL)
        print(Fore.GREEN + response.text)
    except requests.RequestException:
        print(Fore.CYAN + "Welcome to Yala Claim Script!")

# Read accounts from file
def read_auth_file():
    if not os.path.exists(AUTH_FILE):
        return []

    with open(AUTH_FILE, "r") as file:
        accounts = []
        for line in file:
            name, token = line.strip().split("|")
            accounts.append({"name": name, "token": token})
        return accounts

# Write new account to file
def write_auth_file(name, token):
    with open(AUTH_FILE, "a") as file:
        file.write(f"{name}|{token}\n")
    print(Fore.GREEN + f"Account {name} added successfully!")

# Claim daily points
def claim_daily_points(account):
    try:
        headers = {
            "Authorization": f"Bearer {account['token']}",
            "Accept": "*/*"
        }

        response = requests.post(CLAIM_URL, headers=headers)
        response.raise_for_status()
        print(Fore.BRIGHT_GREEN + f"[Success] Daily check-in for {account['name']}.")

        # Fetch balance and rank
        points_response = requests.get(POINTS_URL, headers=headers)
        points_response.raise_for_status()
        points_data = points_response.json()

        print(Fore.YELLOW + f"\nBerries Balance: {points_data['data']['totalPoints']}")
        print(Fore.BLUE + f"Rank: {points_data['data']['rank']}")
    except requests.RequestException as e:
        print(Fore.RED + f"[Error] Failed to claim for {account['name']}: {str(e)}")

# Show main menu
def show_menu():
    while True:
        print(Fore.CYAN + "\n1. Add Account")
        print("2. Run Once")
        print("3. Claim Every 24h")
        print("4. Exit")

        option = input(Fore.MAGENTA + "Select an option: ")
        clear_screen()

        if option == "1":
            name = input(Fore.YELLOW + "Enter account name: ")
            token = input(Fore.YELLOW + "Enter auth token: ")
            write_auth_file(name, token)

        elif option == "2":
            accounts = read_auth_file()
            for account in accounts:
                claim_daily_points(account)

        elif option == "3":
           print(Fore.LIGHTBLUE_EX + "Starting 24-hour scheduler... Press Ctrl+C to stop.")
            try:
                while True:
                    accounts = read_auth_file()
                    for account in accounts:
                        claim_daily_points(account)
                    time.sleep(24 * 60 * 60)
            except KeyboardInterrupt:
                print(Fore.RED + "\nScheduler stopped.")

        elif option == "4":
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid option. Try again.")

if __name__ == "__main__":
    clear_screen()
    display_banner()
    show_menu()
