import datetime
import os


def write_log(msg):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file = open('logs/log.txt', 'at')
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file.write(date)
    file.write("\n")
    file.write(msg)
    file.write("\n")
    file.write(50 * '-')
    file.write("\n")
    file.close()
