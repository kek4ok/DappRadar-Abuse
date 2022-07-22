import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

#BNB HTTPProvider
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def balance_of(wallet):
    balance = w3.eth.getBalance(wallet)
    balance = w3.fromWei(balance, 'ether')
    print(balance)

    return balance

def token_balance(wallet, name):
    with open("tokens.json", 'r+') as f:
        token = json.load(f)
        f.close()
    abi = json.loads(token[name]["ABI"])
    pvu_contract = token[name]["contract"]
    contract = w3.eth.contract(pvu_contract, abi=abi)
    decimals = contract.functions.decimals().call()
    DECIMALS = 10 ** decimals
    balance = contract.functions.balanceOf(wallet).call()
    balance = w3.fromWei(balance, 'ether')
    print(f'${name} Balance of {wallet} = {balance}')

    return balance

