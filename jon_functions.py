import requests
import time
import json
import csv
import ctypes
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_the_watchlist():

    watchlist = []

    with open('csv/watchlist.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        message_text = ''
        for row in csv_reader:
            if line_count == 0:
                # text = f'Column names are {", ".join(row)}'
                # myposts.append({'text': text})
                line_count += 1

            else:

                price = None
                alert = ''

                for v in json.loads(requests.get("https://api.binance.com/api/v3/ticker/price").content):
                    if v['symbol'] == row[0]+row[1]:
                        price = float(v['price'])
                        if price < float(row[2]):
                            message_text = message_text + '\n' + v['symbol'] + ' is below alert price: ' + str(price) + ' < ' + str(row[3])
                            alert = 'alert below'
                        if price > float(row[3]):
                            message_text = message_text + '\n' + v['symbol'] + ' is above alert price: ' + str(price) + ' > ' + str(row[3])
                            alert = 'alert above: ' + str(price) + ' > ' + str(row[3])
                
                watchlist.append({
                    'coin': row[0],
                    'market': row[1],
                    'below': row[2],
                    'above': row[3],
                    'price': price,
                    'alert': alert,
                })
                line_count += 1

        # text = f'Processed {line_count} lines.'
        #watchlist.append({'text': prices})

        if message_text != '':
            send_me_an_email(message_text)

    return watchlist

def send_me_an_email(message_text):
    port = 465  # For SSL
    password = "22xtr05Jon108"

    # Create a secure SSL context
    context = ssl.create_default_context()
    sender_email = "jon@thanx.it"
    receiver_email = "jon@thanx.it"
    message = """\
    Subject: Hi there

    This message is sent from Python."""
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Python Alert"
    #message["Bcc"] = receiver_email  # Recommended for mass emails
    if message_text == '':
        message_text = """\
        Hi,
        How are you?"""

    part1 = MIMEText(message_text, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL("sofia.svrsh.com", port, context=context) as server:
        server.login("jon@thanx.it", password)
        server.sendmail(sender_email, receiver_email, message.as_string())
