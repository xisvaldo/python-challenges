import logging

import requests

REQUEST_TIMEOUT_SECONDS = 5


# Check how to improve with non-blocking calls (httpx) for studying purposes
def get_public_ip() -> str | None:
    try:
        response = requests.get('https://api.ipify.org/?format=json', timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()["ip"]
    except Exception as exception:
        logging.error(f"Failed to obtain public IP address: {exception}.")
        return None
