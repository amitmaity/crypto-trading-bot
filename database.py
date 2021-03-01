import mysql.connector
import time
from configparser import ConfigParser
import calculator


class Database:
    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read('settings.ini')
        db_host = config_parser.get('database_settings', 'host')
        db_port = config_parser.get('database_settings', 'port')
        db_user = config_parser.get('database_settings', 'user')
        db_pass = config_parser.get('database_settings', 'password')
        db_name = config_parser.get('database_settings', 'database')
        self.mydb = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        self.cursor = self.mydb.cursor(dictionary=True)


class BotConfig(Database):
    bot_config = {}

    def get_bot_configs(self):
        self.cursor.execute("SELECT * FROM config")
        result = self.cursor.fetchall()
        for row in result:
            config_name = row['config_name']
            config_value = row['config_value']
            self.bot_config[config_name] = config_value
        return self.bot_config

    def update_bot_config(self, config_name, config_value):
        sql = "UPDATE config SET config_value = '" + config_value + "' WHERE config_name = '" + config_name + "'"
        self.cursor.execute(sql)
        self.mydb.commit()


class Transaction(Database):
    def get_last_buy_transaction(self):
        self.cursor.execute("SELECT * FROM buy_transactions ORDER BY id DESC")
        result = self.cursor.fetchone()
        return result

    def get_sell_transaction_by_buy_transaction(self, buy_id):
        sql = 'SELECT * FROM sell_transactions WHERE buy_order_ref = %s'
        self.cursor.execute(sql, (buy_id,))
        result = self.cursor.fetchone()
        return result

    def insert_buy_transaction(self, data):
        fill_price = None
        fill_quantity = None
        commission = None
        timestamp = int(time.time())
        if data['status'] == 'FILLED':
            fill = calculator.calculate_average_of_order_fills(data['fills'])
            fill_price = fill['average_price']
            fill_quantity = fill['quantity']
            commission = fill['commission']
        sql = "INSERT INTO buy_transactions (order_id, client_order_id, order_quantity, order_price, status, " \
              "fill_price, fill_quantity, commission, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        val = (data['orderId'], data['clientOrderId'], data['origQty'], data['price'], data['status'], fill_price,
               fill_quantity, commission, timestamp)
        self.cursor.execute(sql, val)
        self.mydb.commit()

    def insert_sell_transaction(self, data, buy_order_ref):
        fill_price = None
        fill_quantity = None
        commission = None
        timestamp = int(time.time())
        if data['status'] == 'FILLED':
            fill = calculator.calculate_average_of_order_fills(data['fills'])
            fill_price = fill['average_price']
            fill_quantity = fill['quantity']
            commission = fill['commission']
        sql = "INSERT INTO sell_transactions (buy_order_ref, order_id, client_order_id, order_quantity, order_price, " \
              "status, fill_price, fill_quantity, commission, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s) "
        val = (buy_order_ref, data['orderId'], data['clientOrderId'], data['origQty'], data['price'], data['status'],
               fill_price, fill_quantity, commission, timestamp)
        self.cursor.execute(sql, val)
        self.mydb.commit()

    def update_buy_transaction(self, order_details):
        sql = "UPDATE buy_transactions SET status = 'FILLED', fill_price = %s, fill_quantity = %s WHERE " \
              "order_id = %s "
        val = (order_details['price'], order_details['executedQty'], order_details['orderId'])
        self.cursor.execute(sql, val)
        self.mydb.commit()

    def update_sell_transaction(self, order_details):
        sql = "UPDATE sell_transactions SET status = 'FILLED', fill_price = %s, fill_quantity = %s WHERE " \
              "order_id = %s "
        val = (order_details['price'], order_details['executedQty'], order_details['orderId'])
        self.cursor.execute(sql, val)
        self.mydb.commit()


class PriceData(Database):
    def insert_price_data(self, rate):
        sql = "INSERT INTO price_data (price, timestamp) VALUES (%s, %s)"
        val = (rate, int(time.time()))
        self.cursor.execute(sql, val)
        self.mydb.commit()

    def get_average_price_in_range(self, minutes_before):
        sql = "SELECT AVG(price) AS avg_price, COUNT(id) AS count FROM price_data WHERE timestamp > %s"
        val = int(time.time()) - (minutes_before * 60)
        self.cursor.execute(sql, (val,))
        result = self.cursor.fetchone()
        return result

    def get_max_price_in_range(self, minutes_before):
        sql = "SELECT MAX(price) AS max_price, COUNT(id) AS count FROM price_data WHERE timestamp > %s"
        val = int(time.time()) - (minutes_before * 60)
        self.cursor.execute(sql, (val,))
        result = self.cursor.fetchone()
        return result
