import binance_apis
import database
import calculator
import custom_logger
import time
import json

# Initialise the objects
db_transaction_obj = database.Transaction()
db_bot_config_obj = database.BotConfig()
db_price_data_obj = database.PriceData()

# Initialise variables
SLEEP_TIME = 5
action = None
bot_config = db_bot_config_obj.get_bot_configs()
coin_pair_symbol = bot_config['base_coin'] + bot_config['quote_coin']

# Main process loop
while True:
    try:
        # Determine the action
        if action is None:
            last_buy_transaction = db_transaction_obj.get_last_buy_transaction()
            if last_buy_transaction is None:
                action = 'BUY'
            else:
                sell_transaction = db_transaction_obj.get_sell_transaction_by_buy_transaction(
                    last_buy_transaction['id'])
                if last_buy_transaction['status'] != 'FILLED':
                    action = 'CHECK_BUY_STATUS'
                elif sell_transaction is None:
                    action = 'SELL'
                elif sell_transaction['status'] != 'FILLED':
                    action = 'CHECK_SELL_STATUS'
                else:
                    action = 'BUY'

        # SELL logic
        if action == 'SELL':
            last_buy_transaction = db_transaction_obj.get_last_buy_transaction()
            buy_price = float(last_buy_transaction['fill_price'])
            price_for_sell = db_price_data_obj.get_price_for_sell()
            if (int(time.time()) - price_for_sell['last_updated']) > 2:
                sell_price = price_for_sell['price']
                current_price = calculator.check_price_for_sell(bot_config, buy_price, sell_price)
                quantity = round(float(last_buy_transaction['fill_quantity']),
                                 int(bot_config['coin_quantity_precision']))
                if current_price is not None:
                    # Log
                    message = "Place sell order of {} coins at rate {}"
                    custom_logger.write_log(message.format(quantity, current_price))
                    # Place sell order
                    result = binance_apis.sell_coin(coin_pair_symbol, quantity, current_price)
                    custom_logger.write_log(json.dumps(result))
                    # make entry in database
                    db_transaction_obj.insert_sell_transaction(result, last_buy_transaction['id'])
                    # Determine next operation
                    action = 'BUY' if result['status'] == 'FILLED' else 'CHECK_SELL_STATUS'
            else:
                custom_logger.write_log('Price data not up to date')
            time.sleep(SLEEP_TIME)

        # BUY logic
        if action == 'BUY':
            price_for_buy = db_price_data_obj.get_price_for_buy()
            if (int(time.time()) - price_for_buy['last_updated']) > 2:
                buy_price = price_for_buy['price']
                price_data = calculator.check_price_for_buy(buy_price, bot_config, db_price_data_obj)
                quote_coin_usage_per_transaction = bot_config['quote_coin_usage_per_transaction']
                quantity = calculator.calculate_coin_quantity(quote_coin_usage_per_transaction, buy_price, bot_config)
                if price_data is not None:
                    # Get price and log
                    buy_price = price_data['current_price']
                    message = "Place buy order of {} coins at rate {}"
                    custom_logger.write_log(message.format(quantity, buy_price))
                    # Place buy order
                    result = binance_apis.buy_coin(coin_pair_symbol, quantity, buy_price)
                    custom_logger.write_log(json.dumps(result))
                    # make entry in database
                    db_transaction_obj.insert_buy_transaction(result)
                    # Determine next operation
                    action = 'SELL' if result['status'] == 'FILLED' else 'CHECK_BUY_STATUS'
            else:
                custom_logger.write_log('Price data not up to date')
            time.sleep(SLEEP_TIME)

        if action == 'CHECK_BUY_STATUS':
            last_buy_transaction = db_transaction_obj.get_last_buy_transaction()
            order_detail = binance_apis.check_order_status(coin_pair_symbol, last_buy_transaction['order_id'])
            if order_detail['status'] == 'FILLED':
                db_transaction_obj.update_buy_transaction(order_detail)
                action = 'SELL'
            time.sleep(SLEEP_TIME)

        if action == 'CHECK_SELL_STATUS':
            last_buy_transaction = db_transaction_obj.get_last_buy_transaction()
            order_detail = binance_apis.check_order_status(coin_pair_symbol, last_buy_transaction['order_id'])
            if order_detail['status'] == 'FILLED':
                db_transaction_obj.update_buy_transaction(order_detail)
                action = 'BUY'
            time.sleep(SLEEP_TIME)

    except Exception as e:
        custom_logger.write_log('Error occurred : ' + str(e))
