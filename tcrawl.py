import os
import aiohttp
from pathlib import Path
from colorama import Fore
from core.syncf import print_colored
from config import NOT_FOUND_FILE, DATA_DIRECTORY, TOR_SOCKS_HOST, TOR_SOCKS_PORT, TEMP_DB_PATH, RETRY_PERIOD
from aiohttp_socks import ProxyConnector
from core.asyncf import recursive_crawler
import asyncio


PROJECT_ROOT = Path(__file__).parent
DATA_DIRECTORY = PROJECT_ROOT / DATA_DIRECTORY
NOT_FOUND_FILE = DATA_DIRECTORY / NOT_FOUND_FILE


async def main():
    # create data/not_found.txt if it does not exist
    not_found_file_path = NOT_FOUND_FILE
    os.makedirs(DATA_DIRECTORY, exist_ok=True)
    try:
        with open(not_found_file_path, 'x', encoding='utf-8') as file:
            file.close()
    except:
        pass
    search_keywords = ["index", "heroin", "meth"]
    base_torch_url = f"http://torch2cjfpa4gwrzsghfd2g6nebckghjkx3bn6xyw6capgj2nqemveqd.onion/"
    proxy_url = f'socks5://{TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}'

    connector = ProxyConnector.from_url(proxy_url)

    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            for keyword in search_keywords:
                url_to_crawl = base_torch_url + "?s=" + keyword
                await recursive_crawler(url_to_crawl, session=session, connector=connector)
            await recursive_crawler(r"http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/", session=session, connector=connector)
    except KeyboardInterrupt:
        print_colored("KeyboardInterrupt received. Exiting...", Fore.RED)
    except Exception as e:
        print_colored(f"Error: {str(e)}", Fore.RED)
    finally:
        # Cleanup: Delete the "temp" folder and its contents
        temp_folder_path = TEMP_DB_PATH
        try:
            for file_name in os.listdir(temp_folder_path):
                file_path = os.path.join(temp_folder_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)

            os.rmdir(temp_folder_path)

        except Exception as e:
            print_colored(f"Error during cleanup: {str(e)}", Fore.RED)

if __name__ == "__main__":
    asyncio.run(main())
