from web3 import Web3

# Define RPC URLs for selected networks
rpc_urls = {
    "bsc": "https://bsc-dataseed.binance.org/", # BSC mainnet rpc
    "ethereum": "https://mainnet.infura.io/",  # eth mainnet rpc
    "base": "https://mainnet.base.org"  # Base Network mainnet rpc
}

# Ask user to choose network
print("Select Network:")
print("1: Binance Smart Chain (BSC)")
print("2: Ethereum")
print("3: Base Network Mainnet")

network_choice = input("Enter the number of your network choice: ").strip()

# Mapping network choice to the corresponding RPC URL
network_mapping = {
    "1": "bsc",
    "2": "ethereum",
    "3": "base"  # Base network mainnet
}

selected_network = network_mapping.get(network_choice, "bsc")  # Default to BSC if invalid choice

# Connect to the selected network
web3 = Web3(Web3.HTTPProvider(rpc_urls[selected_network]))

# Check if the connection was successful
if not web3.is_connected():
    print("Error: Unable to connect to the selected network.")
    exit()

# Get wallet address from user input
wallet_address = input("Enter your wallet address: ").strip()
wallet_address = Web3.to_checksum_address(wallet_address)

# Get contract address from user input
contract_address_input = input("Enter the contract address of the token: ").strip()
contract_address = Web3.to_checksum_address(contract_address_input)

# ABI for balanceOf (standard ERC-20 method)
abi = [{
    "constant": True,
    "inputs": [{"name": "_owner", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "balance", "type": "uint256"}],
    "type": "function"
}]

# Contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Query balance
try:
    balance = contract.functions.balanceOf(wallet_address).call()
    human_balance = balance / (10 ** 18)  # Assuming 18 decimals (adjust if needed)
    print(f"Your token balance on {selected_network}: {human_balance:.4f}")
except Exception as e:
    print(f"Error: {e}")
