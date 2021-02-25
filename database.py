import mysql.connector
import time
from configparser import ConfigParser


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
        self.cursor = self.mydb.cursor()


class BotConfig(Database):
    bot_config = {}

    def get_bot_configs(self):
        self.cursor.execute("SELECT * FROM config")
        result = self.cursor.fetchall()
        for row in result:
            self.bot_config[row[0]] = row[1]
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
        sql = 'SELECT * FROM sell_transactions WHERE buy_order_ref = ' + buy_id
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result


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
