import requests
from configparser import ConfigParser
import time
import hmac
import hashlib
from urllib.parse import urlencode

# Parse config
config_parser = ConfigParser()
config_parser.read('settings.ini')
api_base_url = config_parser.get('exchange_settings', 'api_base_url')


def get_avg_price(symbol):
    url = api_base_url + '/api/v3/avgPrice'
    resp = requests.get(url, 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data


def get_24h_price(symbol):
    url = api_base_url + '/api/v3/ticker/24hr'
    resp = requests.get(url, 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data


def get_current_price(symbol):
    url = api_base_url + '/api/v3/ticker/price'
    resp = requests.get(url, 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data


def buy_coin(symbol, quantity, price):
    url = api_base_url + '/api/v3/order'
    api_key = config_parser.get('exchange_settings', 'api_key')
    secret_key = config_parser.get('exchange_settings', 'secret_key')
    secret_key = bytes(secret_key, 'utf-8')
    payload = {'symbol': symbol, 'side': 'BUY', 'type': 'LIMIT', 'quantity': quantity, 'price': price,
               'timeInForce': 'GTC', 'timestamp': int(time.time() * 1000)}
    total_params = urlencode(payload)
    total_params = bytes(total_params, 'utf-8')
    signature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
    payload['signature'] = signature
    headers = {'X-MBX-APIKEY': api_key}
    resp = requests.post(url, data=payload, headers=headers)
    data = resp.json()
    return data
