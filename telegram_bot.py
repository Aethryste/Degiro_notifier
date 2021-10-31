# Richard Algra | exam-exercise | 'Degiro notifier'
"""
This script repeatedly checks if there are any trigger-points in the data from 'DN_database.csv',
If specific conditions are met, this script will use a Telegram bot to notify the user.
"""
# Resources
import telebot
import config  # settings and personal data.
import pandas as pd
import schedule
from math import dist

bot = telebot.TeleBot(config.API_KEY)
running = True

# Variables in which I store the value that the last (associated) notification was based on. (spam prevention)
checkpoints_account = [
    ['checkpoint_account_total', 0],
    ['checkpoint_available_funds', 0],
    ['checkpoint_total_change', 0],
    ['checkpoint_daily_change', 0]
]
# List of all (owned) stock info. STOCKS = (acronym, average price bought at, notification checkpoint)
stock_list = [
    ['checkpoint_ABT', (116.98 * 2), 0],
    ['checkpoint_T', (29.87 * 10), 0],
    ['checkpoint_BRMK', (9.6214 * 70), 0],
    ['checkpoint_GNL', (16.74 * 15), 0],
    ['checkpoint_LXP', (11.52 * 20), 0],
    ['checkpoint_PLD', (108.24 * 2), 0],
    ['checkpoint_SPG', (66.55 * 5), 0],
    ['checkpoint_STAG', (21.32 * 5), 0],
    ['checkpoint_WY', (37.70 * 1), 0]
]


# Functions
def init_bot_schedule():
    """
    Collection of scheduled tasks. (check function intervals)
    :return:
    """
    schedule.every(1).day.at('15:30').do(notify_market_open)
    schedule.every(1).day.at('22:00').do(notify_market_close)
    schedule.every(3).seconds.do(check_available_funds)
    schedule.every(3).seconds.do(check_daily_change)
    schedule.every(3).seconds.do(check_stock_difference)


def notify_market_open():
    """
    Sends a notification when the market (NYSE) opens.
    :return:
    """
    bot.send_message(config.PID, 'NYSE just opened!')


def notify_market_close():
    """
    Sends a notification when the market (NYSE) closes.
    :return:
    """
    bot.send_message(config.PID, 'NYSE just closed.')


def notify_bot_start():
    """
    Sends a notification at bot startup.
    :return:
    """
    bot.send_message(config.PID, '[ONLINE]')


def notify_bot_exit():
    """
    Sends a notification at bot exit.
    :return:
    """
    bot.send_message(config.PID, '[OFFLINE]')


def manager_checkpoints():
    """
    Function to set all checkpoints to the last collected values, prevents needless notifications at startup.
    :return:
    """
    # Sets all account related checkpoints.
    df = pd.read_csv('DN_database.csv', usecols=[0, 1, 2, 3])
    for index in checkpoints_account:
        if index[1] == 0:
            latest_value = float(str(df.values.tolist()[-1][checkpoints_account.index(index)]).replace(",", "."))
            index[1] = latest_value

    # Sets all stock-price checkpoints.
    for index in range(4, (len(stock_list)) + 4):
        df = pd.read_csv('DN_database.csv', usecols=[index])
        latest_value = float(str(df.values.tolist()[-1][0]).replace(",", "."))
        if stock_list[index-4][2] == 0:
            stock_list[index-4][2] = latest_value


def check_available_funds():
    """
    This function checks if there has been a change in 'available funds', notifies if triggered.
    :return:
    """
    df = pd.read_csv('DN_database.csv', usecols=[1])
    latest_value = df.values.tolist()[-1][0]
    latest_value = float(str(latest_value).replace(",", "."))
    difference = round(abs(dist([latest_value], [checkpoints_account[1][1]])))

    if checkpoints_account[1][1] > latest_value:
        signum_check = 'down'
    else:
        signum_check = 'up'

    if latest_value >= config.trigger_available_funds or config.trigger_available_funds:
        if difference >= config.trigger_available_funds:
            bot.send_message(config.PID, f'[Available funds] {signum_check}!]\n'
                                         f'[Change] €{difference}\n'
                                         f'[Current] €{latest_value}')
            checkpoints_account[1][1] = latest_value


def check_daily_change():
    """
    This function checks if there has been a change in 'daily change', notifies if triggered.
    :return:
    """
    df = pd.read_csv('DN_database.csv', usecols=[3])
    latest_value = df.values.tolist()[-1][0]
    latest_value = float(str(latest_value).replace(",", "."))

    additional_df = pd.read_csv('DN_database.csv', usecols=[0])
    total_value = additional_df.values.tolist()[-1][0]
    total_value = float(str(total_value).replace(",", "."))
    value_difference = round(abs(dist([latest_value], [checkpoints_account[3][1]])), 2)

    if checkpoints_account[3][1] > latest_value:
        signum_check = 'down'
    else:
        signum_check = 'up'

    if latest_value >= config.trigger_daily_change or latest_value <= config.trigger_daily_change:
        if abs(dist([latest_value], [checkpoints_account[3][1]])) >= config.trigger_daily_change:
            bot.send_message(config.PID, f'[Account worth {signum_check}!]\n'
                                         f'[Change] €{value_difference}\n'
                                         f'[Current] €{total_value}')
            checkpoints_account[3][1] = latest_value


def check_stock_difference():
    """
    This function checks stock-value difference in percentage.
    :return:
    """
    for index in range(4, (len(stock_list))+4):
        df = pd.read_csv('DN_database.csv', usecols=[index])
        latest_value = float(str(df.values.tolist()[-1][0]).replace(",", "."))
        stock_tag = str(stock_list[index-4][0])[11:]

        checkpoint = stock_list[index-4][2]
        percentage = round(abs((latest_value - checkpoint) / checkpoint) * 100, 2)

        if latest_value < checkpoint:
            signum_check = 'down'
        elif latest_value > checkpoint:
            signum_check = 'up'

        if percentage >= config.trigger_stock_difference:
            bot.send_message(config.PID, f'[{stock_tag}] {signum_check}!\n'
                                         f'[{percentage}%]\n'
                                         f'assets are currently worth:'
                                         f'[€{latest_value}]')
        stock_list[index-4][2] = latest_value


# telegram_bot.py loop, replaced by main.py.
if __name__ == '__main__':
    print('This script is managed by main.py')
