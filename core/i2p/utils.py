import requests


def get_i2p_ip():
    test_url = "http://httpbin.org/ip"
    proxy_url = "http://localhost:4444"

    session = requests.session()
    session.proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        response = session.get(test_url)
        print(response.text.split('"')[3])
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    get_i2p_ip()
