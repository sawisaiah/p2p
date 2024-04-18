import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Your Telegram Bot API token
TOKEN = "6953412767:AAGKDKQqLgbOmg3ndzqSPoFgysDcoPbG2Vk"
# URL where your bot's code is hosted (GitHub Pages)
URL = "https://github.com/sawisaiah/p2p.git"

def start(update, context):
    update.message.reply_text("Welcome to the MMK Calculator Bot! Please enter the amount of USD you want to convert.")

def handle_input(update, context):
    amount_usd = float(update.message.text.strip())
    update.message.reply_text("Please choose a payment method: KBZPay, AYA Pay, Wave Pay, or KBZ Bank Transfer.")

def fetch_binance_data():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "asset": "USDT",
        "fiat": "MMK",
        "page": 1,
        "rows": 10
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def process_binance_data(data):
    if data is None:
        return None
    # Extract relevant information from the data
    for ad in data["data"]["advertisements"]:
        price = float(ad["price"])
        payment_methods = [method["name"] for method in ad["tradeMethods"]]
        tradable_quantity = float(ad["maxTradeAmount"])
        pay_time_limit = ad["payTimeLimit"]
        max_single_transaction_amount = float(ad["maxTradeAmount"])
        min_single_transaction_amount = float(ad["minTradeAmount"])
        # Perform any additional processing or filtering as needed
        # Return the extracted information
        return price, payment_methods, tradable_quantity, pay_time_limit, max_single_transaction_amount, min_single_transaction_amount

def handle_payment_method(update, context):
    payment_method = update.message.text.strip()
    data = fetch_binance_data()
    if data is not None:
        price, payment_methods, tradable_quantity, pay_time_limit, max_single_transaction_amount, min_single_transaction_amount = process_binance_data(data)
        if payment_method in payment_methods:
            # Perform calculations based on fetched data and user input
            # Show the result to the user
            update.message.reply_text(f"Based on your choice of {payment_method}, the price of USDT is {price} MMK, and you can trade up to {tradable_quantity} USDT.")
        else:
            update.message.reply_text("Sorry, the selected payment method is not available.")
    else:
        update.message.reply_text("Sorry, unable to fetch Binance data at the moment. Please try again later.")

def set_webhook():
    response = requests.post(f"https://api.telegram.org/bot{TOKEN}/setWebhook", data={"url": URL})
    print(response.text)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_input))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_payment_method))

    set_webhook()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

