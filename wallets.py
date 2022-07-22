import datetime
import json
import time

from dapp_inter import sign_message, send_signed_message, get_message, add_email, get_verif_link, identify, \
    participate_in_airdrop
from bnb_chain import balance_of, token_balance

with open("email.txt", 'r') as r:
    emails = r.readlines()


def ftom_txt_to_json():
    with open("wallets.txt", 'r') as f:
        lines = f.readlines()

    for line in lines:
        keys = line[:-1].split(":")
        print(lines.index(line))
        with open("base.json", 'r+') as f:
            data = json.load(f)
            f.close()

        data[f'{lines.index(line)}'] = {'address': f"{keys[0]}", 'private_key': f"{keys[1]}"}

        with open("base.json", 'w') as f:
            json.dump(data, f, indent=4)


def add_token_to_base():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()
    for i in data:
        wallet = data[i]['address']
        private_key = data[i]['private_key']
        message = get_message(wallet)
        signature = sign_message(message, private_key)
        token = send_signed_message(wallet, signature, message)
        data[i]["token"] = token

        with open("base.json", 'w') as f:
            json.dump(data, f, indent=4)

        print(i)


def add_verif_link():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()

    for i in data:
        if data[i].get("verif_link") == None:
            print(i)
            print(datetime.datetime.now())
            token = data[i]['token']
            data[i]["email"] = emails[int(i)][:-1]
            while 1:
                try:
                    add_email(emails[int(i)][:-1], token)
                    verif_link = get_verif_link()
                    break
                except IndexError:
                    time.sleep(10)

            data[i]["verif_link"] = verif_link

            with open("base.json", 'w') as f:
                json.dump(data, f, indent=4)
            print(emails[int(i)][:-1])


def check_email_confirmation():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()
    for i in data:
        if data[i].get("email_confirmed") == None:  # For first scan change False to None
            wallet = data[i]['address']
            private_key = data[i]['private_key']
            token = data[i]['token']
            try:
                status = identify(token)
            except KeyError:
                message = get_message(wallet)
                signature = sign_message(message, private_key)
                token = send_signed_message(wallet, signature, message)
                data[i]["token"] = token
                with open("base.json", 'w') as f:
                    json.dump(data, f, indent=4)
                    f.close()
                status = identify(token)

            if status:
                data[i]["email_confirmed"] = True
            else:
                data[i]["email_confirmed"] = False

            print(i)


def resend_verif_message():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()

    for i in data:
        if data[i].get("email_confirmed") == False:
            print(i)
            print(datetime.datetime.now())
            token = data[i]['token']
            data[i]["email"] = emails[int(i)][:-1]
            while 1:
                try:
                    add_email(emails[int(i)][:-1], token)
                    verif_link = get_verif_link()
                    break
                except IndexError:
                    time.sleep(10)

            data[i]["verif_link"] = verif_link

            with open("base.json", 'w') as f:
                json.dump(data, f, indent=4)
            print(emails[int(i)][:-1])


def join_airdrop():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()
    for i in data:
        print(i)
        wallet = data[i]['address']
        token = data[i]["token"]
        email = data[i]["email"]
        participate_in_airdrop(email, wallet, token)


def get_all_bnb_balances():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()

    for i in data:
        wallet = data[i]["address"]
        balance = balance_of(wallet)


def get_token_balance():
    with open("base.json", 'r+') as f:
        data = json.load(f)
        f.close()

    for i in data:
        wallet = data[i]["address"]
        balance = token_balance(wallet, "PVU")
