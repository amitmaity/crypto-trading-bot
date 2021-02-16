import binance_apis


def get_price_for_buy(ticker_price, bot_config, db_price_data_obj):
    avg_min = int(bot_config['average_minute'])
    current_price = float(ticker_price['lastPrice'])
    max_price_data = db_price_data_obj.get_max_price_in_range(avg_min)
    if max_price_data[1] < (avg_min * 12):
        return None
    max_price = max_price_data[0]
    if current_price < max_price:
        price_diff = max_price - current_price
        price_diff_percent = price_diff / max_price * 100
        if price_diff_percent > float(bot_config['buy_price_diff_percentage']):
            return {'current_price': current_price, 'average_price': max_price}
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
