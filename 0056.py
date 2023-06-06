import yfinance as yf
import ta
import smtplib
from email.mime.text import MIMEText
import datetime

# Query stock information
stock = yf.Ticker("0056.TW")

# Get historical stock prices
hist = stock.history(period="max")

# Calculate monthly KD indicator
kd = ta.momentum.StochasticOscillator(high=hist['High'], low=hist['Low'], close=hist['Close'], window=9, smooth_window=3)
hist['slowk'], hist['slowd'] = kd.stoch(), kd.stoch_signal()

# Calculate golden cross and death cross for monthly KD
golden_cross = (hist['slowk'][-2] < hist['slowd'][-2]) & (hist['slowk'][-1] > hist['slowd'][-1])
death_cross = (hist['slowk'][-2] > hist['slowd'][-2]) & (hist['slowk'][-1] < hist['slowd'][-1])

# Determine whether to buy or sell
if golden_cross:
    decision = "Sell"
elif death_cross:
    decision = "Buy"
else:
    decision = "Hold"

# Record current timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# Compose email message
message = f"{timestamp}: {decision}, K: {hist['slowk'][-1]}, D: {hist['slowd'][-1]}"
msg = MIMEText(message)
msg['Subject'] = '0056 Trading Decision'
msg['From'] = 'adanyao@gmail.com'
msg['To'] = 'autoicash2023@gmail.com'

# SMTP server and email parameters
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "autoicash2023@gmail.com"
sender_password = "zgwcpumiolaoksgd"
receiver_email = "adanyao@gmail.com"

# Send email notification
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

