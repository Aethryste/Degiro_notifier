# Degiro_notifier
A project that web-scrapes portfolio data from 'Degiro' and notifies the user through 'Telegram'.

IMPORTANT:
To summarise: 
Most of this project still relies on personal data and therefrore cannot be run (yet) by another user.
In future versions I will purge all personal data from web_scraper.py and telegram_bot.py and have both scripts import
all necessary data from config.py, in which the user can place their own data without having to alter code in other files.

specific:
-In order to run this project it it necessary to install a version of chrome-webdriver that matches the browser version you've got installed.
-The path to this file must be specified in web_scraper.py.
-Although 'the title contains the recipe', an account on Degiro is needed, specify your credentials in config.py.
  //the contents of DN_database.csv should be removed, they serve as an example.
-A telegram account is also necessary, you'll need to specify your chat-ID in config.py.
-Currently it is also necessary to run a telegram bot, your API-key can be specified in config.py.
-From telegram_bot.py > stock_list: The contents of this list should be changed to the users own portfolio.

PLANNED:
-[after exam] remove the exam related function from main.py.
-[after exam] remove all exam related docstrings and comments.
-purge all personal data from web_scraper.py and telegram_bot.py and have both scripts import all necessary data from config.py
-make all scripts modular to the contents of config.py. (all fixed values replaced by len(config.list))
-Have to user specify the markets the wish to use, for notification purposes. (currently the script only notifies open and close of NYSE.)
