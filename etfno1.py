# -*- coding: utf-8 -*-
#!/usr/bin/python3
import pandas as pd
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import sys

print("Python Interpreter Path:")
print(sys.executable)

print("Python Module Paths:")
for path in sys.path:
    print(path)


def calculate_kd(data):
    close = data['Close']
    high = data['High']
    low = data['Low']
    n = 9
    m1 = 3
    m2 = 3
    rsv = (close - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min()) * 100
    k = rsv.ewm(com=m1).mean()
    d = k.ewm(com=m2).mean()
    kd = k[-1]
    return kd

def trade(stock_price):
    data = yf.download('0050.TW', period='1mo')  # 下载台股代码为 0050.TW 的股票数据

    # 计算 KD 值
    kd = calculate_kd(data)
    
    # 打印 KD 值
    print("當前 KD 值為：{:.2f}".format(kd))


    # 根据 KD 值进行交易操作
    if kd < 20:
        print("買入 {} 股票".format(stock_price))
    elif kd > 80:
        print("賣出 {} 股票".format(stock_price))

    else:
        print("不進行操作")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = "autoicash2023@gmail.com"
    sender_password = "zgwcpumiolaoksgd"

    receiver_email = "adanyao@gmail.com"

    message = "目前 KD 值為 %.2f" % kd
    msg = MIMEText(message)
    msg['Subject'] = '每日股票ETF'
    msg['From'] = 'adanyao@gmail.com'
    msg['To'] = 'autoicash2023@gmail.com'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == '__main__':
    trade(50)

