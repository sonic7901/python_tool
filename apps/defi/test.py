from functools import lru_cache

from eth_utils import keccak

from tabulate import tabulate

from web3 import Web3

RPC_URL = 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'
#
# ETHRPC_URL = 'https://bsc-dataseed.binance.org'
#
# BSC
# https://peckshield.medium.com/bearn-fi-incident-inconsistent-asset-denomination-between-vault-strategy-9b24b68ab1c0
#
# TRANSACTIONS = ['0x603b2bbe2a7d0877b22531735ff686a7caad866f6c0435c37b7b49e4bfd9a36c']
#
# https://peckshield.medium.com/bogged-finance-incident-root-cause-analysis-718d53faad5c
#
TRANSACTIONS = ['0x50105b6d07b4d738cd11b4b8ae16943bed09c7ce724dc8b171c74155dd496c25',
                '0xd65025a2dd953f529815bd3c669ada635c6001b3cc50e042f9477c7db077b4c9',
                '0xea37b320843f75a8a849fdf13cd357cb64761a848d48a516c3cac5bbd6caaad5']

w3 = Web3(Web3.HTTPProvider(RPC_URL))


@lru_cache(maxsize=32)
def get_token_symbol(token_address):
    token_contract = w3.eth.contract(token_address,
                                     abi=[{
                                         "constant": False,
                                         "inputs": [],
                                         "name": "symbol",
                                         "outputs": [{
                                             "name": "",
                                             "type": "string"}],
                                         "payable": False,
                                         "stateMutability": "view",
                                         "type": "function"}, {
                                         "constant": False,
                                         "inputs": [],
                                         "name": "decimals",
                                         "outputs": [{
                                             "name": "",
                                             "type": "uint8"}],
                                         "payable": False,
                                         "stateMutability": "view",
                                         "type": "function"}])
    return token_contract.functions.symbol().call(), token_contract.functions.decimals().call()


transfer_hash = keccak(b'Transfer(address,address,uint256)')
symbols = set()
balances = {}
for TRANSACTION in TRANSACTIONS:
    receipt = w3.eth.getTransactionReceipt(TRANSACTION)
    for log in receipt.logs:
        if log.topics[0] == transfer_hash:
            symbol, decimals = get_token_symbol(log['address'])
            symbols.add(symbol)
            form_address = log.topics[1].hex()
            to_address = log.topics[2].hex()
            value = int(log.data, 16)
            balance = balances.setdefault(to_address, {})
            if symbol in balance:
                balance[symbol] += value / (10 ** decimals)
            else:
                balance[symbol] = value / (10 ** decimals)
            balance = balances.setdefault(form_address, {})
            if symbol in balance:
                balance[symbol] -= value / (10 ** decimals)
            else:
                balance[symbol] = -value / (10 ** decimals)
symbols = list(symbols)
symbols.sort()
headers = ['Address', *symbols]
table = []
symbol_balances = {}
for address, balance in balances.items():
    address = f'0x{address[26:]}'
    row = [address, *[balance.get(s, 0) for s in symbols]]
    for s in symbols:
        if s in symbol_balances:
            symbol_balances[s] += balance.get(s, 0)
        else:
            symbol_balances[s] = balance.get(s, 0)
    table.append(row)
row = ['sum', *[symbol_balances.get(s, 0) for s in symbols]]
table.append(row)
print(tabulate(table, headers=headers))
