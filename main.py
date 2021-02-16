import binance_apis
import database
import calculator
import logger
import time

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
    if action is None:
        last_transaction = db_transaction_obj.get_last_transaction()
        if last_transaction is None or last_transaction['action'] == 'SELL':
            action = 'BUY'
        else:
            action = 'SELL'

    if action == 'SELL':
        current_price = calculator.get_price_for_sell(coin_pair_symbol, bot_config, buy_price)
        if current_price is not None:
            logger.write_log('sell_price: ' + current_price)
            action = 'BUY'

    if action == 'BUY':
        ticker_price = binance_apis.get_24h_price(coin_pair_symbol)
        db_price_data_obj.insert_price_data(ticker_price['lastPrice'])
        price_data = calculator.get_price_for_buy(ticker_price, bot_config, db_price_data_obj)
        if price_data is not None:
            buy_price = price_data['current_price']
            average_price = price_data['average_price']
            message = "buy_price: {}, average_price: {}"
            logger.write_log(message.format(buy_price, average_price))
            action = 'SELL'

    time.sleep(SLEEP_TIME)
