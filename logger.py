import datetime


def write_log(msg):
    file = open('logs/log.txt', 'at')
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    file.write(date)
    file.write("\n")
    file.write(msg)
    file.write("\n")
    file.write(50 * '-')
    file.write("\n")
    file.close()
