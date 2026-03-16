import requests


REQUEST_TIMEOUT_SECONDS=5

async def get_public_ip() -> str:
    response = await requests.get('https://api.ipify.org/?format=json', timeout=REQUEST_TIMEOUT_SECONDS).json()
    return response["ip"]