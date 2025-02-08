import requests
import sqlite3
import schedule
import time

def main():
    while True:
        update_prices()
        print("in main")
        time.sleep(5)

def update_prices():
    print("in update prices")
    conn = sqlite3.connect("crypto_alerts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT token_name, token_id, buy_price, current_price, percent_increase, alerted_75, alerted_100, alerted_150, alerted_200 FROM tokens")
    tokens = cursor.fetchall()
    
    for token_name, token_id, buy_price, current_price, percent_increase, alerted_75, alerted_100, alerted_150, alerted_200 in tokens:
        new_price = get_price(token_id)
        
        if new_price is None:
            continue

        percent_increase = ((new_price - buy_price) / buy_price) * 100

        cursor.execute("UPDATE tokens SET current_price = ?, percent_increase = ? WHERE token_id = ?", (new_price, percent_increase, token_id))
        check_alerts(token_id, percent_increase, alerted_75, alerted_100, alerted_150, alerted_200)

    conn.commit()
    conn.close()

def get_price(token_id):
    print("in get price")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        #return data.get(token_id, {}).get("usd", "Price not available")
        return 1000000
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def check_alerts(token_id, percent_increase, alerted_75, alerted_100, alerted_150, alerted_200):
    print("in check alerts")
    conn = sqlite3.connect("crypto_alerts.db")
    cursor = conn.cursor()

    #Alert on discord if the token has increased by 75%
    if percent_increase >= 75 and not alerted_75:
        print("in 75")
        send_discord_alert(f"🚀 {token_id} is up **{percent_increase:.2f}%**! Time to think about selling")
        cursor.execute("UPDATE tokens SET alerted_75 = 1 WHERE token_id = ?", (token_id))
    #Reset the alert to 0 if the token has decreased below 75%
    if percent_increase < 75 and alerted_75:
        cursor.execute("UPDATE tokens SET alerted_75 = 0 WHERE token_id = ?", (token_id))

    if percent_increase >= 100 and not alerted_100:
        print("in 100")
        send_discord_alert(f"💰 {token_id} is up **{percent_increase:.2f}%**! Your investment has doubled!")
        cursor.execute("UPDATE tokens SET alerted_100 = 1 WHERE token_id = ?", (token_id))
    if percent_increase < 100 and alerted_100:
        cursor.execute("UPDATE tokens SET alerted_100 = 0 WHERE token_id = ?", (token_id))

    if percent_increase >= 150 and not alerted_150:
        print("in 150")
        send_discord_alert(f"🔥 {token_id} has hit **150% gains**! It is currently up **{percent_increase:.2f}%**! 🚀💰")
        cursor.execute("UPDATE tokens SET alerted_150 = 1 WHERE token_id = ?", (token_id))
    if percent_increase < 150 and alerted_150:
        cursor.execute("UPDATE tokens SET alerted_150 = 0 WHERE token_id = ?", (token_id))

    if percent_increase >= 200 and not alerted_200:
        print("in 200")
        send_discord_alert(f"💎 {token_id} is up **{percent_increase:.2f}%**! Time to secure profits! 💰")
        cursor.execute("UPDATE tokens SET alerted_200 = 1 WHERE token_id = ?", (token_id))
    if percent_increase < 200 and alerted_200:
        cursor.execute("UPDATE tokens SET alerted_200 = 0 WHERE token_id = ?", (token_id))

    conn.commit()
    conn.close()

def send_discord_alert(message):
    print("in send discord alert")
    WEBHOOK_URL = "https://discordapp.com/api/webhooks/1337159579745783953/MRHmc77vK8775jYr_l3NJfOJned0nVJstn-i2HC7nEI1OuI-m4ZRzdlqGhVnnqJBdTG1"
    data = {"content": message, "username": "Captain Hook"}
    requests.post(WEBHOOK_URL, json=data)

main()