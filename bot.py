import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]

CHANNELS = {
    "bitcoin": os.environ["CHAT_BTC"],
    "ethereum": os.environ["CHAT_ETH"],
    "solana": os.environ["CHAT_SOL"],
}

URL = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": ",".join(CHANNELS.keys()),
    "vs_currencies": "usd",
    "include_24hr_change": "true",
    "include_market_cap": "true"
}

data = requests.get(URL, params=params, timeout=30).json()

EMOJIS = {
    "bitcoin": "₿",
    "ethereum": "Ξ",
    "solana": "◎"
}

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        },
        timeout=30
    )

for coin, channel in CHANNELS.items():
    price = data[coin]["usd"]
    change = data[coin].get("usd_24h_change", 0)
    market_cap = data[coin].get("usd_market_cap", 0)

    direction = "🟢" if change >= 0 else "🔴"

    msg = f"""
{direction} <b>{coin.upper()} UPDATE</b>

{EMOJIS[coin]} Price: ${price:,.2f}

24h Change: {change:.2f}%

Market Cap:
${market_cap:,.0f}

#CRYPTO
"""

    send_message(channel, msg)
