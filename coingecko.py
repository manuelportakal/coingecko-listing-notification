import smtplib
import sys
import requests
import schedule
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def job():
    log_file = open("log.txt", "w")
    tokens = {}
    newurl = "https://www.coingecko.com/en/coins/recently_added"
    html = requests.get(newurl).text
    soup = bs(html, "lxml")
    tags = soup.findAll("tbody")[0]

    global count, body
    count = 1
    body = "A new coin has been listed!\n"
    for tr in tags.find_all('tr'):
    
        name = tr.find_all('a', class_="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between", recursive=True)[0]
        price = tr.find_all('span', class_="no-wrap", recursive=True)[0]
        date = tr.find_all('td', class_="trade p-0 col-market pl-2 text-center", recursive=True)[0]
    
        if "minutes" in  date.text.replace("\n", "") and int(''.join(filter(str.isdigit, date.text))) < 15 :
            tokens[count] = {'id': str(count), 'name': name.text.replace("\n", "") }
            tokens[count]['price'] = price.text.replace("\n", "")
            tokens[count]['date'] = date.text.replace("\n", "")
            tokens[count]['link'] = "https://www.coingecko.com" + name['href']
            body += "\nName: " + tokens[count]['name'] + "\nCurrent Price: " + tokens[count]['price'] + "\nListing time: " + tokens[count]['date'] + " minutes ago" + "\nLink: " + tokens[count]['link'] + "\n\n"

        count += 1
    
    if len(tokens) >= 1:
        try:
            mail = smtplib.SMTP("smtp.gmail.com",587)
            mail.ehlo()
            mail.starttls()
            mail.login("sender_email@gmail.com", "sender_password")
            mesaj = MIMEMultipart()
            mesaj["From"] = "sender@gmail.com"
            mesaj["To"] = "my_email@gmail.com"
            mesaj["Subject"] = "Coingecko Listing Notification"

            body_text = MIMEText(body, "plain")  #
            mesaj.attach(body_text)
            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            print("Email sent successfully.\n")
            mail.close()
            print("\a")
            print(body)
            log_file.write(body)

        except:
            print("Error:", sys.exc_info()[0])
    else:
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        print(str(dt_string) +": There is no new coin")
        log_file.write(str(dt_string) +": There is no new coin")

    log_file.close()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)