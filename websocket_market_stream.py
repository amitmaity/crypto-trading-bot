from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import database
import json
import custom_logger
import time

db_bot_config_obj = database.BotConfig()
db_price_data_obj = database.PriceData()

bot_config = db_bot_config_obj.get_bot_configs()
coin_pair_symbol = bot_config['base_coin'] + bot_config['quote_coin']

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
binance_websocket_api_manager.create_stream(['ticker'], [coin_pair_symbol])

while True:
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer:
        stream_data = json.loads(oldest_stream_data_from_stream_buffer)
        if stream_data.get('data') is not None:
            price = stream_data['data']['c']
            low = stream_data['data']['l']
            high = stream_data['data']['h']
            db_price_data_obj.insert_price_data(price, low, high)
        else:
            custom_logger.write_log(oldest_stream_data_from_stream_buffer)
    else:
        time.sleep(0.2)
