import requests
from bs4 import BeautifulSoup
import smtplib
import time
url = 'https://www.amazon.com/Upgrade-3500Lumens-Projector-Supported-Smartphone/dp/B07YBRGLGW/ref=sr_1_9?crid' \
      '=3LWI7WTR8IQGH&keywords=projector&qid=1578782732&sprefix=projector%2Caps%2C212&sr=8-9 '

headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.88 Safari/537.36 '
           }


def check_price():
    page = requests.get(url, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    price = soup2.find(id="priceblock_ourprice").get_text()
    title = soup2.find(id="title").get_text()
    converted_price = float(price[1:6])

    if (converted_price < 59.99):
        send_mail()
    print(converted_price)
    print(title.strip())

    if (converted_price < 59.99):
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('niantic1029@gmail.com', 'cuglpbvcqdnzjefk')
    subject = 'Price Fell!'
    body = 'Check the link: https://www.amazon.com/Upgrade-3500Lumens-Projector-Supported-Smartphone/dp/B07YBRGLGW/ref=sr_1_9?crid' \
           '=3LWI7WTR8IQGH&keywords=projector&qid=1578782732&sprefix=projector%2Caps%2C212&sr=8-9 '
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'niantic1029@gmail.com',
        'dowdp282@gmail.com',
        msg
    )
    print('EMAIL HAS BEEN SENT')
    server.quit()

while (True):
    check_price()
    time.sleep(86400)