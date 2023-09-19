import requests

# Set up Alchemy API endpoint
ALCHEMY_API_KEY = "<your api key>"
ALCHEMY_URL = f"https://eth-goerli.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

# Make a request to Alchemy to get the latest block number
response = requests.get(f"{ALCHEMY_URL}/blocks/latest")
data = response.json()
block_number = int(data["result"]["number"], 16)

print(f"Latest block number: {block_number}")