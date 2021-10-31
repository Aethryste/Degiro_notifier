# Richard Algra | exam-exercise | 'Degiro notifier'
"""
This script collects portfolio data through web-scraping with 'Selenium' and stores said data in 'DN_database.csv'.
Then 'telegram_bot.py' notifies the user through 'telegram' notifications if any trigger-points are met.
NOTE: I've received permission from Degiro to web-scrape my own data.
"""
# Resources
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import config  # settings and personal data.

URL = 'https://trader.degiro.nl/login/'
data_accountTotal = ''
data_availableFunds = ''
data_total_change = ''
data_daily_change = ''
data_stock_values = []
dict_of_unlabeled = {}
df_stocks = pd.DataFrame()
df_account = pd.DataFrame()

# Website elements, If <URL> code changes some day and Xpath, class-names, ect, change then only edit the strings below.
ID_loginUsername = 'username'
ID_loginPassword = 'password'
CLASS_accountSummary = '_2zDWRdoX'
CLASS_stockPrices = 'boBUSoUu'
XPATH_portfolio_page = "//*[@href='#/portfolio']"
XPATH_accountTotal = "//*[@data-field='total']"
XPATH_availableFunds = "//*[@data-field='availableToSpend']"
XPATH_total_change = "//*[@data-field='totalPl']"
XPATH_daily_change = "//*[@data-field='todayPl']"

# Selenium web-driver init.
PATH = 'C:\Program Files (x86)\chromedriver.exe'  # Path to the chrome web-driver on my own machine.
driver = webdriver.Chrome(PATH)
driver.get(URL)
driver.set_window_size(600, 1000)


# All functions.
def login_to_website():
    """
    Function that sends 'username' and 'password' from config.py to the login-form.
    :return:
    """
    element = driver.find_element_by_name(ID_loginUsername)
    element.send_keys(config.USERNAME)
    element = driver.find_element_by_name(ID_loginPassword)
    element.send_keys(config.PASSWORD)
    element.send_keys(Keys.RETURN)


def site_navigation():
    """
    Navigates to portfolio page and expands the account summary, revealing all elements of interest.
    :return:
    """
    selection = driver.find_element_by_xpath(XPATH_portfolio_page)
    selection.send_keys(Keys.RETURN)
    selection = driver.find_element_by_class_name(CLASS_accountSummary)
    selection.send_keys(Keys.RETURN)


def get_account_total():
    """
    Get current 'account total' value.
    :return:
    """
    global data_accountTotal
    selection = driver.find_element_by_xpath(XPATH_accountTotal)
    raw_current = selection.get_attribute('title')
    data_accountTotal = raw_current.replace(".", "")


def get_account_available():
    """
    Get current 'available funds' value.
    :return:
    """
    global data_availableFunds
    selection = driver.find_element_by_xpath(XPATH_availableFunds)
    raw_current = selection.get_attribute('title')
    data_availableFunds = raw_current.replace(".", "")


def get_total_change():
    """
    Get 'account total' (win/loss) value.
    :return:
    """
    global data_total_change
    selection = driver.find_element_by_xpath(XPATH_total_change)
    raw_current = selection.get_attribute('title')
    current = raw_current.replace("-", "").replace("+", "").replace(".", "")
    # checks if the value is meant as gain or loss.
    if selection.get_attribute('data-positive') == 'true':
        data_total_change = ('+' + current)
    elif selection.get_attribute('data-positive') == 'false':
        data_total_change = ('-' + current)


def get_daily_change():
    """
    Get account daily (win/loss) value.
    :return:
    """
    global data_daily_change
    selection = driver.find_element_by_xpath(XPATH_daily_change)
    raw_current = selection.get_attribute('title')
    current = raw_current.replace("-", "").replace("+", "").replace(".", "")
    # checks if the value is meant as gain or loss.
    if selection.get_attribute('data-positive'):
        data_daily_change = ('+' + current)
    elif selection.get_attribute('data-negative'):
        data_daily_change = ('-' + current)


def get_owned_stock_prices():
    """
    Get all (owned) stock prices, turn into dataframe.
    :return:
    """
    global df_stocks, data_stock_values, dict_of_unlabeled
    selection = driver.find_elements_by_class_name(CLASS_stockPrices)
    for element in selection:
        if element.get_attribute('data-field') == 'value':
            raw_current = element.get_attribute('title')
            current = raw_current.replace("-", "").replace("+", "").replace(".", "")
            data_stock_values.append(current)
    # Data to dataframe.
    df_stocks = pd.DataFrame(
        data={
            # All (manually) labeled stocks.
            'ABT': data_stock_values[0],
            'T': data_stock_values[1],
            'BRMK': data_stock_values[2],
            'GNL': data_stock_values[3],
            'LXP': data_stock_values[4],
            'PLD': data_stock_values[5],
            'SPG': data_stock_values[6],
            'STAG': data_stock_values[7],
            'WY': data_stock_values[8]
        },
        columns=('ABT', 'T', 'BRMK', 'GNL', 'LXP', 'PLD', 'SPG', 'STAG', 'WY'),
        index=[0])
    # Remove collected (manually labeled) data from list.
    for i in range(len(df_stocks.columns)):
        data_stock_values.pop(0)
    # If any values left in list, add to dataframe through dict as unlabeled(num).
    if data_stock_values:
        dict_of_unlabeled = {}
        for i in range(len(data_stock_values)):
            dict_of_unlabeled["unlabeled_%s" % i] = data_stock_values[0]
            data_stock_values.pop(0)

    unlabeled_df = pd.DataFrame(dict_of_unlabeled, index=[0])
    df_stocks = pd.concat([df_stocks, unlabeled_df], axis=1)


def save_data():
    """
    Combine all dataframes, write data to 'DN_database.csv'.
    :return:
    """
    # Account data to dataframe.
    global df_account, df_stocks, data_accountTotal, data_availableFunds, data_daily_change, data_total_change
    df = pd.read_csv('DN_database.csv')
    df_account = pd.DataFrame(
        data={'account_total': data_accountTotal,
              'available_funds': data_availableFunds,
              'total_change': data_total_change,
              'daily_change': data_daily_change},
        columns=('account_total', 'available_funds', 'total_change', 'daily_change'),
        index=[0])

    # append dataframes, save to 'DN_database.csv'.
    df_update = pd.concat([df_account, df_stocks], axis=1, join='inner')
    df = pd.concat([df, df_update])
    df.to_csv('DN_database.csv', index=False)     # PEP8:warning turns out to be a bug in pycharm (source=stackoverflow)


# web_scraper.py loop, replaced by main.py.
if __name__ == '__main__':
    print('This script is managed by main.py')
