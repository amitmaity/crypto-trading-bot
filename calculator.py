import binance_apis
import logger


def get_price_for_buy(ticker_price, bot_config, db_price_data_obj):
    avg_min = int(bot_config['average_minute'])
    current_price = float(ticker_price['lastPrice'])
    max_price_data = db_price_data_obj.get_max_price_in_range(avg_min)
    if max_price_data['count'] < (avg_min * 12):
        return None
    max_price = max_price_data['max_price']
    if current_price < max_price:
        price_diff = max_price - current_price
        price_diff_percent = price_diff / max_price * 100
        message = "BUY_CHECK|max_price: {}, current_price: {}, price_dif_percentage: {}"
        logger.write_log(message.format(max_price, current_price, price_diff_percent))
        if price_diff_percent > float(bot_config['buy_price_diff_percentage']):
            return {'current_price': current_price}
        else:
            return None
    else:
        return None


def get_price_for_sell(coin_pair_symbol, bot_config, buy_price):
    result = binance_apis.get_current_price(coin_pair_symbol)
    current_price = float(result['price'])
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


def calculate_coin_quantity(total_amount, rate):
    quantity = float(total_amount) / float(rate)
    return quantity
