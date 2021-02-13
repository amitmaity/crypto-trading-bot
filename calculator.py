import binance_apis


def get_price_for_buy(coin_pair_symbol, bot_config):
    result = binance_apis.get_24h_price(coin_pair_symbol)
    weighted_avg_price = float(result['weightedAvgPrice'])
    print(result)
    result = binance_apis.get_current_price(coin_pair_symbol)
    current_price = float(result['price'])
    print(result)
    if current_price < weighted_avg_price:
        price_diff = weighted_avg_price - current_price
        price_diff_percent = price_diff / weighted_avg_price * 100
        if price_diff_percent > float(bot_config['buy_price_diff_percentage']):
            return {'current_price': current_price, 'average_price': weighted_avg_price}
        else:
            return None
    else:
        return None


def get_price_for_sell(coin_pair_symbol, bot_config, buy_price):
    result = binance_apis.get_current_price(coin_pair_symbol)
    current_price = float(result['price'])
    print(result)
    if current_price > buy_price:
        price_diff = current_price - buy_price
        price_diff_percent = price_diff / buy_price * 100
        if price_diff_percent > float(bot_config['sell_price_diff_percentage']):
            return {'current_price': current_price}
        else:
            return None
    else:
        return None
