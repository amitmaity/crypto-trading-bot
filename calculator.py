import binance_apis
import logger
import json


def get_price_for_buy(ticker_price, bot_config, db_price_data_obj):
    price_range_minutes = int(bot_config['price_range_minutes'])
    current_price = float(ticker_price['lastPrice'])
    max_price_data = db_price_data_obj.get_max_price_in_range(price_range_minutes)
    if max_price_data['count'] < (price_range_minutes * 10):
        logger.write_log('Not enough price data, count: ' + str(max_price_data['count']))
        return None
    max_price = float(max_price_data['max_price'])
    if current_price < max_price and current_price < float(ticker_price['highPrice']):
        price_diff = max_price - current_price
        price_diff_percent = price_diff / max_price * 100
        price_diff_24hr_high = float(ticker_price['highPrice']) - current_price
        price_diff_24hr_high_percent = price_diff_24hr_high / float(ticker_price['highPrice']) * 100
        message = "BUY_CHECK|max_price: {}, current_price: {}, price_diff_percent: {}, 24hr_high_diff_percent: {}"
        logger.write_log(message.format(max_price, current_price, price_diff_percent, price_diff_24hr_high_percent))
        cfg_buy_percent = float(bot_config['buy_price_diff_percentage'])
        cfg_24hr_percent = float(bot_config['buy_price_diff_percentage_from_24hr_high'])
        if price_diff_percent > cfg_buy_percent and price_diff_24hr_high_percent >= cfg_24hr_percent:
            return {'current_price': current_price}
        else:
            return None
    else:
        return None


def get_price_for_sell(coin_pair_symbol, bot_config, buy_price, ticker_price):
    result = binance_apis.get_current_price(coin_pair_symbol)
    current_price = float(ticker_price['lastPrice'])
    buy_price = float(buy_price)
    if current_price > buy_price:
        price_diff = current_price - buy_price
        price_diff_percent = price_diff / buy_price * 100
        message = "SELL_CHECK|current_price: {}, price_dif_percentage: {}"
        logger.write_log(message.format(current_price, price_diff_percent))
        if price_diff_percent > float(bot_config['sell_price_diff_percentage']):
            return current_price
        else:
            return None
    else:
        return None


def calculate_average_of_order_fills(fills):
    total_price = 0
    total_quantity = 0
    commission = 0
    for fill in fills:
        total_price += (float(fill['price']) * float(fill['qty']))
        total_quantity += float(fill['qty'])
        commission += float(fill['commission'])
    average_price = total_price / total_quantity
    return {'average_price': average_price, 'quantity': total_quantity, 'commission': commission}


def calculate_coin_quantity(total_amount, rate, bot_config):
    quantity = float(total_amount) / float(rate)
    precision = int(bot_config['coin_quantity_precision'])
    quantity = round(quantity, precision)
    return quantity
