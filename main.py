#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib, ssl
from pythonping import ping
from libs.host import address
import yaml

def init():

    with open('/usr/src/app/config.yaml') as f:
        try:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)

            for doc in docs:
                for k, v in doc.items():
                    if k == "hosts":
                        set_hosts(v)
        except yaml.YAMLError as exc:
            print(exc)


def set_hosts(hosts):

    global hosts_list
    hosts_list = []

    for item in hosts:
        ac = item.split(":")
        hosts_list.append(address(ac[0], ac[1]))

def send_message(message):
    #define the SMTP server separately here:
    port = 465 
    smtp_server = "smtp.gmail.com"


    # specify the sender’s and receiver’s email addresses
    sender = ""
    receiver = ""
    # type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to  automatically insert variables in the text
    SUBJECT = "ALERT! Mach536 Cameras Down!"
    TEXT = f"""\

    One of the Mach536 Check Fixture Cameras are not connected!"""
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    try:
        #send your message with credentials specified above
        with smtplib.SMTP(smtp_server, port) as server:
            server.login(login, password)
            server.sendmail(sender, receiver, message)
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))

def ping_host(address):

    status = ping_url(address.address)
    
    if status != address.status:
        send_message(address.comment + ( " is unresolwed" if status is None else " is up" if status else " is down"))
        address.status = status

def ping_url(url):

    try:
        response_list = ping(url)
    except:
        return None

    return sum(1 for x in response_list if x.success) > 0

def main():

    init()

    while True:

        for host in hosts_list:
            ping_host(host)

if __name__ == '__main__':
    main()