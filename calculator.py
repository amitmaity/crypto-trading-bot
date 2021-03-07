import custom_logger
import json
import time


def check_price_for_buy(buy_price, bot_config, db_price_data_obj):
    price_range_days = int(bot_config['average_price_range_days'])
    current_price = float(buy_price)
    starting_timestamp = int(time.time()) - (price_range_days * 86400)
    minimum_data_points = int(bot_config['minimum_data_points_per_minute']) * 60 * 24 * price_range_days
    avg_price_data = db_price_data_obj.get_average_price_in_range(starting_timestamp)
    if avg_price_data['count'] < minimum_data_points:
        custom_logger.write_log('Not enough price data, count: ' + str(avg_price_data['count']))
        return None
    avg_price = float(avg_price_data['avg_price'])
    if current_price < avg_price:
        message = "BUY_CHECK|avg_price: {}, current_price: {}"
        custom_logger.write_log(message.format(avg_price, current_price))
        return {'current_price': current_price}
    else:
        return None


def check_price_for_sell(bot_config, buy_price, current_price):
    current_price = float(current_price)
    buy_price = float(buy_price)
    if current_price > buy_price:
        price_diff = current_price - buy_price
        price_diff_percent = price_diff / buy_price * 100
        message = "SELL_CHECK|current_price: {}, price_dif_percentage: {}"
        custom_logger.write_log(message.format(current_price, price_diff_percent))
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
