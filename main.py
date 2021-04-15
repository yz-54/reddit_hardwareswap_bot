import praw
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

KEYWORD = '3080'
sender_address = ""
sender_pass = ""
receiver_address = ""

reddit = praw.Reddit('swapBot')
hardwareswap = reddit.subreddit("hardwareswap")
# appleswap = reddit.subreddit("appleswap")

lastTitle_hws = ""
title_hws = ""
text_hws = ""
url_hws = ""

def send_email(post_url: str, sub: str, keyword: str):
    mail_content = post_url
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    subject = keyword + " found in " + sub
    message['Subject'] = subject
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


while True:
    for submission in hardwareswap.new(limit=1):
        title_hws = submission.title
        text_hws = submission.selftext
        url_hws = submission.url

        if title_hws == lastTitle_hws:
            break
        else:
            lastTitle_hws = title_hws
            print("title: ", title_hws)
            print("url: ", url_hws)

            start = title_hws.find('[H]')+3
            end = title_hws.find('[W]')
            subTitle = title_hws[start:end]
            print("subtitle: ", subTitle)

            if re.search(KEYWORD, subTitle, re.IGNORECASE):
                print("keyword found: ", KEYWORD)
                send_email(url_hws, "hardwareswap", KEYWORD)

            print("---------------------------------\n")

