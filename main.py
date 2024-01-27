from colorama import Fore, Style
import sys
from pathlib import Path
import platform
import warnings
from pyfiglet import Figlet

from core.tor.utils import main as tor_ip_utility
from core.i2p.utils import main as i2p_ip_utility

warnings.filterwarnings("ignore")


def print_banner():
    custom_fig = Figlet(font='ansi_shadow')
    banner_text = custom_fig.renderText('Shadow\n  Sight')
    print(f"{Fore.GREEN}\n{banner_text}{Style.RESET_ALL}")


def display_system_info():
    print(f"\n{Fore.CYAN}System Information:{Style.RESET_ALL}")
    print(f"  OS: {platform.system()} ")
    print(f"  Processor: {platform.processor()}")
    print(f"  Python Version: {platform.python_version()}")
    print(f"  Architecture: {platform.architecture()}")


def display_menu():
    print("\nChoose an option:")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}1{Fore.CYAN}]{Style.RESET_ALL} Start web crawling through Tor")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}2{Fore.CYAN}]{Style.RESET_ALL} Start web crawling through I2P")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}3{Fore.CYAN}]{Style.RESET_ALL} Start web crawling through both Tor and I2P")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}4{Fore.CYAN}]{Style.RESET_ALL} Run Tor IP Utility")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}5{Fore.CYAN}]{Style.RESET_ALL} Run I2P IP Utility")
    print(
        f"  {Fore.CYAN}[{Style.RESET_ALL}6{Fore.CYAN}]{Style.RESET_ALL} Exit")


def main():
    print_banner()
    display_system_info()

    while True:
        try:
            display_menu()
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                tor_ip_utility()
            elif choice == "5":
                i2p_ip_utility()
            elif choice == "6":
                print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(
                    f"\n{Fore.RED}Invalid choice. Please enter a number between 1 and 5.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()