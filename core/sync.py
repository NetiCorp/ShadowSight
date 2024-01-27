from datetime import datetime
import csv
import os
import secrets
import string
from fake_useragent import UserAgent
import time
from colorama import init, Fore

TEMP_DB_PATH = 'temp'
CSV_FILE_PATH = os.path.join('data', 'data.csv')

def print_colored(message, color=Fore.WHITE):
    print(color + message + Fore.RESET)
    
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

def generate_secure_random_string(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    return ''.join(char if char not in invalid_chars else '_' for char in filename)

def save_data_to_file(data, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, sanitize_filename(filename))
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)
    print(f"Data saved to: {filepath}")

def save_url_to_csv(filename, url):
    with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'url', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not os.path.exists(CSV_FILE_PATH):
            writer.writeheader()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        writer.writerow(
            {'filename': filename, 'url': url, 'timestamp': timestamp})
        print_colored(
            f"URL saved to CSV: filename={filename}, url={url}", Fore.GREEN)
        
def save_url_to_temp_db(url):
    os.makedirs(TEMP_DB_PATH, exist_ok=True)
    temp_db_file = os.path.join(TEMP_DB_PATH, "scraped.txt")

    # Check if the URL is already in the database
    if url in load_urls_from_temp_db():
        print_colored(f"URL already in temporary database: {url}", Fore.YELLOW)
        return

    with open(temp_db_file, 'a', encoding='utf-8') as file:
        file.write(f"{url}\n")
    print_colored(f"URL saved to temporary database: {url}", Fore.GREEN)
    
def load_urls_from_temp_db():
    urls_set = set()
    temp_db_file_path = os.path.join(TEMP_DB_PATH, "scraped.txt")
    if os.path.exists(temp_db_file_path):
        with open(temp_db_file_path, 'r', encoding='utf-8') as file:
            urls_set.update(line.strip() for line in file if line.strip())
    return urls_set

def clear_temp_db_data():
    while True:
        time.sleep(24*60*60)  # Sleep for 10 minutes (600 seconds)
        try:
            with open(os.path.join(TEMP_DB_PATH, "scraped.txt"), 'w', encoding='utf-8') as file:
                file.truncate()
        except Exception as e:
            pass
        print_colored("Temporary database cleared.", Fore.YELLOW)
        
def save_url_to_not_found(url):
    not_found_file_path = 'data/not_found.txt'
    with open(not_found_file_path, 'a', encoding='utf-8') as file:
        file.write(f"{url}\n")
    print_colored(f"URL saved to not found file: {url}", Fore.RED)

def remove_url_from_not_found(url):
    not_found_file_path = 'data/not_found.txt'
    try:
        with open(not_found_file_path, 'r', encoding='utf-8') as file:
            not_found_urls = [line.strip() for line in file if line.strip()]

        if url in not_found_urls:
            not_found_urls.remove(url)

            with open(not_found_file_path, 'w', encoding='utf-8') as file:
                for not_found_url in not_found_urls:
                    file.write(f"{not_found_url}\n")
            print_colored(
                f"Removed URL from not found file: {url}", Fore.GREEN)
        else:
            print_colored(
                f"URL not found in not found file: {url}", Fore.YELLOW)
    except FileNotFoundError:
        print_colored("Not found file not found.", Fore.RED)
    except Exception as e:
        print_colored(
            f"Error while removing URL from not found file: {str(e)}", Fore.RED)