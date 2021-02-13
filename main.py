import binance_apis
import database
import calculator
import logger
import time

# Initialise the objects
db_transaction_obj = database.Transaction()
db_bot_config_obj = database.BotConfig()

# Initialise variables
action = None
bot_config = db_bot_config_obj.get_bot_configs()
coin_pair_symbol = bot_config['base_coin'] + bot_config['quote_coin']
SLEEP_TIME = 5

# Main process loop
while True:
    if action is None:
        last_transaction = db_transaction_obj.get_last_transaction()
        if last_transaction is None or last_transaction['action'] == 'SELL':
            action = 'BUY'
        else:
            action = 'SELL'

    if action == 'BUY':
        price_data = calculator.get_price_for_buy(coin_pair_symbol, bot_config)
        if price_data is not None:
            buy_price = price_data['current_price']
            average_price = price_data['average_price']
            message = "buy_price: {}, average_price: {}"
            logger.write_log(message.format(buy_price, average_price))
            action = 'SELL'
            time.sleep(SLEEP_TIME)

    if action == 'SELL':
        current_price = calculator.get_price_for_sell(coin_pair_symbol, bot_config, buy_price)
        if current_price is not None:
            logger.write_log('sell_price: ' + current_price)
            exit(0)

    time.sleep(SLEEP_TIME)

