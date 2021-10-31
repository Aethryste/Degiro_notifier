# Richard Algra | exam-exercise | 'Degiro notifier'
"""
This config file (.py) is used to configure settings and conceal sensitive data,
sensitive data used within this project is imported through this file and thereby never shown directly.
"""
# Degiro_notifier settings
function_interval = 2  # <int> seconds to wait, preferred number may change depending on connection speed.
loop_interval = 10  # <int> seconds to wait before collecting the next set of data.
trigger_available_funds = 0.5  # notification threshold, float(1.00) == 1 euro.
trigger_daily_change = 0.4  # notification threshold, int(1) == 1 euro.
trigger_stock_difference = 0.20  # Notification threshold, float(1.00) == 1%.

# Degiro settings
USERNAME = ''
PASSWORD = ''

# Telegram settings
API_KEY = ''
PID = 0000000000  # personal chat_ID
