import requests
import json
from configparser import ConfigParser

api_base_url = 'https://api.binance.com/'


def get_avg_price(symbol):
    resp = requests.get('https://api.binance.com/api/v3/avgPrice', 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data


def get_24h_price(symbol):
    resp = requests.get('https://api.binance.com/api/v3/ticker/24hr', 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data


def get_current_price(symbol):
    resp = requests.get('https://api.binance.com/api/v3/ticker/price', 'symbol=' + symbol)
    data = resp.json()
    status_code = resp.status_code
    return data

