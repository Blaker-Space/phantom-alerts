import requests
import json

class Token:
    def __init__(self, name, mint, pool, purchasePrice, currentPrice):
        self.name = name
        self.mint = mint
        self.pool = pool
        self.purchasePrice = purchasePrice
        self.currentPrice = currentPrice

        def to_dict(self):
        return {
            "name": self.name,
            "mint": self.mint,
            "pool": self.pool,
            "purchasePrice": self.purchasePrice,
            "currentPrice": self.currentPrice
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["mint"], data["pool"], data["purchasePrice"], data["currentPrice"])


def save_tokens(tokens, filename="tokens.json"):
    with open(filename, "w") as f:
        json.dump([token.to_dict() for token in tokens], f, indent=4)

def load_tokens(filename="tokens.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Token.from_dict(item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

tokens = load_tokens()

new_token = Token("DogWifHat", "WiFv5NqsFw...", 0.10, 100)
tokens.append(new_token)

save_tokens(tokens)

for token in tokens:
    print(f"Token: {token.name}, Amount: {token.amount}, Purchase Price: ${token.purchase_price}")

"""
def get_token_id(contract_address):
    url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{contract_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["id"]  # Get the token's CoinGecko ID
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def get_price_from_coingecko(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get(token_id, {}).get("usd", "Price not available")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


token = PurchasedToken("VALENTINE", "841xNZH2ACGbtDZAkwpvMSa3fYYnw3p575vnTn5Mpump", None, 0.0000592, None)


for i in len(token_mints):
    token_price = get_price_from_coingecko(token_mints[0])

if(tokenID == None):
    exit()
else:
    tokenPrice = get_price_from_coingecko(tokenID)
    if(tokenPrice == None):
        exit()
    else:
        print(f"Solana price: ${tokenPrice}")


pool_id = "CRHt3gCYPWKEnBCJvKWna1UsgMgq47PZp4WcXDQrisVE"

"""