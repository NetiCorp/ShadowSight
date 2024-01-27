import requests
from ..syncf import print_colored
from colorama import Fore


def get_i2p_ip():
    test_url = "http://httpbin.org/ip"
    proxy_url = "http://localhost:4444"
    print_colored("Requesting i2P IP...", Fore.YELLOW)
    session = requests.session()
    session.proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        response = session.get(test_url)
        print_colored("i2P IP: {}".format(
            response.text.split('"')[3]), Fore.GREEN)
    except Exception as e:
        print_colored(f"Error: {str(e)}")


main = get_i2p_ip

if __name__ == "__main__":
    get_i2p_ip()
