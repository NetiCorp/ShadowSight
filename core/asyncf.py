import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import os
import time
from pathlib import Path
from colorama import Fore
from core.syncf import load_urls_from_temp_db, print_colored, get_random_user_agent, generate_secure_random_string, save_data_to_file, save_url_to_csv, save_url_to_temp_db, save_url_to_not_found, remove_url_from_not_found
from config import NOT_FOUND_FILE, DATA_DIRECTORY, TOR_SOCKS_HOST, TOR_SOCKS_PORT, TEMP_DB_PATH, RETRY_PERIOD, ARCHIVE_DIRECTORY

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIRECTORY = PROJECT_ROOT / DATA_DIRECTORY
NOT_FOUND_FILE = DATA_DIRECTORY / NOT_FOUND_FILE
TEMP_DB_PATH = PROJECT_ROOT / TEMP_DB_PATH
ARCHIVE_DIRECTORY = PROJECT_ROOT / ARCHIVE_DIRECTORY


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def web_crawler_with_saving_and_urls(id, url, session, connector):
    flag = False
    if ".onion" in str(url) or ".i2p" in str(url):
        flag = True
    if not flag:
        return set()
    if not id:
        id = 1
    scraped_urls = load_urls_from_temp_db()
    if url in scraped_urls:
        print_colored(f"URL already scraped: {url}", Fore.YELLOW)
        return set()

    try:
        # Add a random user agent to the headers
        headers = {'User-Agent': get_random_user_agent()}

        # Use a try-except block to catch CancelledError
        try:
            async with session.get(url, headers=headers, allow_redirects=True) as response:
                response.raise_for_status()  # Raise an HTTPError for bad responses

                if response.status == 200:
                    # Get the final URL after following redirects
                    final_url = str(response.url)
                    print_colored(
                        f"Final URL after redirects: {final_url}", Fore.GREEN)
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    base_url = final_url
                    urls_set = {
                        urljoin(base_url, link.get('href'))
                        for link in soup.find_all('a', href=True)
                        if not link.get('href').startswith('mailto:')
                    }
                    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    filename = f"{id}_{timestamp}_{generate_secure_random_string(8)}.html"
                    save_data_to_file(await response.text(), ARCHIVE_DIRECTORY, filename)
                    # Save the final URL to CSV
                    save_url_to_csv(filename, final_url)
                    # Save the final URL to the temporary database
                    save_url_to_temp_db(final_url)
                    if final_url != url:
                        save_url_to_temp_db(url)
                    return urls_set
                else:
                    print_colored(
                        f"Failed to retrieve the page. Status code: {response.status}", Fore.RED)
                    save_url_to_not_found(url)
                    return set()

        except asyncio.CancelledError:
            # print_colored(f"Request for URL cancelled: {url}", Fore.YELLOW)
            return set()

    except Exception as e:
        print_colored(
            f"Request failed for URL: {url}\nError: {e}", Fore.RED)
        return set()


async def recursive_crawler(url, session, connector, depth=1, max_depth=3, limit=False):
    if limit and depth > max_depth:
        return

    print_colored(f"\nCrawling URL (Depth {depth}): {url}", Fore.CYAN)
    found_urls = await web_crawler_with_saving_and_urls(depth, url, session, connector)

    tasks = [recursive_crawler(next_url, session, connector,
                               depth + 1, max_depth, limit) for next_url in found_urls]
    await asyncio.gather(*tasks)


async def retry_scrape_not_found_urls(session, connector):
    not_found_file_path = NOT_FOUND_FILE
    try:
        with open(not_found_file_path, 'r', encoding='utf-8') as file:
            not_found_urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print_colored("Not found file not found.", Fore.RED)
        return

    for url in not_found_urls:
        print_colored(
            f"\nRetrying to scrape not found URL: {url}", Fore.YELLOW)
        await web_crawler_with_saving_and_urls(None, url, session, connector)
        # If the scraping is successful, remove the URL from not_found.txt
        # if url not in load_urls_from_temp_db():
        remove_url_from_not_found(url)


async def periodic_retry_scrape():
    print_colored("Periodic Retry Enabled", Fore.CYAN)
    while True:
        time.sleep(RETRY_PERIOD)
        try:
            connector = ProxyConnector.from_url(
                f'socks5://{TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}')

            async with aiohttp.ClientSession(connector=connector) as session:
                await retry_scrape_not_found_urls(session, connector)
        except Exception as e:
            print_colored(f"Error during periodic retry: {str(e)}", Fore.RED)
