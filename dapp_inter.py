import imaplib
import re
import time

from eth_account.messages import encode_defunct
from eth_account import Account
import json
import requests
import cloudscraper

headers = {}


def get_message(wallet):
    url = f"https://auth.dappradar.com/apiv4/users/nonce/{wallet}"
    response = requests.get(url, headers=headers).json()
    nonnce = response["nonce"]
    message = f"I am signing my one-time nonce: {nonnce}"
    return message


def sign_message(msg, private_key):
    msghash = encode_defunct(text=msg)
    key = private_key
    signature = str(Account.sign_message(msghash, key).signature.hex())
    return signature


def send_signed_message(wallet, signature, message):

    url = f"https://auth.dappradar.com/apiv4/users/sign_metamask/{wallet}"
    data = {
        "signature": signature,
        "message": message
    }
    response = requests.post(url, headers=headers, json=data).json()
    token = response["token"]
    print(response)
    return token


def add_email(email, token):
    ses = requests.Session()
    url = 'https://auth.dappradar.com/apiv4/users/add-email'
    ses.headers = {}
    data = {
        "token": token,
        "email": email
    }

    scraper = cloudscraper.create_scraper(sess=ses, browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    response = scraper.post(url, json=data).json()
    print(response)


def identify(token):
    ses = requests.Session()
    url = 'https://auth.dappradar.com/apiv4/users/identify'
    headers = {}

    scraper = cloudscraper.create_scraper(sess=ses, browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True,
        'headers': headers
    })
    response = scraper.get(url, headers=headers).json()
    status = response["user"]["meta"]["emailConfirmed"]

    return status


def get_verif_link():
    time.sleep(15)
    imap_server = 'imap.gmail.com'
    email_address = 'login'
    email_password = 'password'

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, email_password)
    print('Login to gmail was successful!')

    imap.select('Inbox')
    _, msgnums = imap.search(None, '(FROM "DappRadar")')

    ids = msgnums[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    latest_email_id = id_list[-1]  # get the latest

    result, data = imap.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822) for the given ID

    message = str(data[0][1])

    url = re.findall(r'"https://u9941984\.ct\.sendgrid\.net/ls/click.{400,500}3D" ', message)
    url = url[0].replace('"', '').replace("=\\r\\n", "").replace("upn=3D", "upn=")
    # print(url)

    return str(url)


def verif_email(verurl):
    ses1 = requests.Session()
    headers = {}

    scraper2 = cloudscraper.create_scraper(sess=ses1, browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True,
        'headers': headers
    })
    response = scraper2.post(verurl, headers=headers)
    print(response.text)


def participate_in_airdrop(email, wallet, token):
    url = "https://backoffice-new.dappradar.com/airdrops/94/participate"
    headers = {}
    data = {
        "email": email,
        "wallet": wallet
    }
    response = requests.post(url, headers=headers, json=data).json()
    print(response)


