import json
import requests
from web3 import Web3
import solcx
from eth_account import Account
from eth_account.signers.local import LocalAccount

# Set up Alchemy provider
ALCHEMY_API_KEY = "<your api key>"
ALCHEMY_URL = f"https://eth-goerli.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

# Solidity contract source code in a separate .sol file
contract_file_path = "contracts/IoTNode.sol"

# Read the contract source code from the file
# with open(contract_file_path, "r") as f:
#     contract_source_code = f.read()

def compile_source_file(file_path):
    solcx.install_solc(version='0.8.9')
    solcx.set_solc_version('0.8.9')
    with open(file_path, 'r') as f:
        source = f.read()
        print(source)
    return solcx.compile_source(source)

# Compile the contract
compiled_contract = compile_source_file(contract_file_path)
contract_interface = compiled_contract["<stdin>:IoTNode"]

# Set up web3 instance
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# Set up account and private key
private_key = "<wallet address>"
account: LocalAccount = Account.from_key(private_key)

# Deploy the contract
contract = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
deploy_txn = contract.constructor().build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 2000000,
})

signed_txn = w3.eth.account.sign_transaction(deploy_txn, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Get the contract address from the transaction receipt
contract_address = tx_receipt["contractAddress"]

print(f"Contract deployed at address: {contract_address}")