import requests
import sqlite3
import schedule
import sys


def main():
    create_table()
    if(len(sys.argv) > 4 or len(sys.argv) < 3):
        print("Usage: python update_tokens.py add <token_name> <mint_address>")
        print("Usage: python update_tokens.py remove <token_name>")
        print("Usage: python update_tokens.py view all")
        print("Usage: python update_tokens.py view <token_name>")
    if sys.argv[1] == "add":
        add_token(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "remove":
        remove_token(sys.argv[2])
    elif sys.argv[1] == "view":
        if sys.argv[2] == "all":
            display_tokens()
        elif sys.argv[2] is not None:
            conn = sqlite3.connect("crypto_alerts.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tokens WHERE token_name = ?", (sys.argv[2],))
            token = cursor.fetchone()
            if token:
                print(token)
            else:
                print(f"No token found with name {sys.argv[2]}")
            conn.close()


# SQLite database setup and access functions
def create_table():
    conn = sqlite3.connect("crypto_alerts.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_name TEXT,
            token_id TEXT UNIQUE,
            buy_price REAL,
            current_price REAL,
            percent_increase REAL,
            alerted_75 BOOLEAN DEFAULT 0,
            alerted_100 BOOLEAN DEFAULT 0,
            alerted_150 BOOLEAN DEFAULT 0,
            alerted_200 BOOLEAN DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()

def display_tokens():
    conn = sqlite3.connect("crypto_alerts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tokens")
    tokens = cursor.fetchall()
    for token in tokens:
        print(token)
    conn.close()

def add_token(token_name, token_id):
    
    buy_price = get_price(token_id)
    if not buy_price:
        print("Could not fetch token price.")
        return
    
    conn = sqlite3.connect("crypto_alerts.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO tokens (token_name, token_id, buy_price, current_price, percent_increase) VALUES (?, ?, ?, ?, ?)",
                  (token_name, token_id, buy_price, buy_price, 0))
        conn.commit()
        print(f"Added {token_name} to tracking at ${buy_price}")
    except sqlite3.IntegrityError:
        print("Token already exists.")
    conn.close()

def remove_token(token_name):
    conn = sqlite3.connect("crypto_alerts.db")
    c = conn.cursor()
    c.execute("DELETE FROM tokens WHERE token_name = ?", (token_name,))
    conn.commit()
    conn.close()
    print(f"{token_name} removed.")

#CoinGecko API usage for updating prices
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_token_id(mint_address):
    url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{mint_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["id"]  # Get the token's CoinGecko ID
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
def get_price(token_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get(token_id, {}).get("usd", "Price not available")
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

main()