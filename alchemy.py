from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
import solcx

# Set up Alchemy provider
ALCHEMY_API_KEY = "<your api key>"
ALCHEMY_URL = f"https://eth-goerli.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

contract_address = "0xD8598D75A193214a578b1b32Cf0CdA2596149453"

node_address = "0x8eC83fb001e99649D69861bC2bD7CE4Dc85bFF26"
private_key = "<address of the wallet>"
account = Account.from_key(private_key)

# Set up web3 instance
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

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

contract = w3.eth.contract(address=contract_address, abi=contract_interface["abi"])

# Simulate IoT node readings
reading_value = 45

# Add a reading to the smart contract
add_reading_txn = contract.functions.addReading(reading_value).build_transaction({
    "from": node_address,
    "nonce": w3.eth.get_transaction_count(node_address),
    "gas": 2000000,
    "gasPrice": w3.to_wei(10, "gwei")
})

signed_txn = w3.eth.account.sign_transaction(add_reading_txn, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)


# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Get the reading count for the node
reading_count = contract.functions.getReadingCount(node_address).call()
print(f"Reading added. Reading count: {reading_count}")

block_number = int(input("Insert the number of the required block: "))
if block_number != '':
    values_block = contract.functions.getReading(node_address, block_number).call()
    print(values_block)
    print(f"Value of the sensor:{values_block[1]}, at {values_block[0]}")