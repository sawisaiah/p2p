import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler

WELCOME, ENTER_AMOUNT, CHOOSE_PAYMENT_METHOD = range(3)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Welcome to Changer4U money transfer.\n"
        "Please enter the USDT amount you would like to transfer:"
    )
    return ENTER_AMOUNT

def enter_amount(update: Update, context: CallbackContext) -> int:
    amount = update.message.text
    context.user_data['amount'] = amount
    keyboard = [
        [InlineKeyboardButton("KBZPay1", callback_data='KBZPay1')],
        [InlineKeyboardButton("AYAPay", callback_data='AYAPay')],
        [InlineKeyboardButton("WaveMoney", callback_data='WaveMoney')],
        [InlineKeyboardButton("uabpay", callback_data='uabpay')],
        [InlineKeyboardButton("CBPay", callback_data='CBPay')],
        [InlineKeyboardButton("Onepay", callback_data='Onepay')],
        [InlineKeyboardButton("BANK", callback_data='BANK')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your payment method:', reply_markup=reply_markup)
    return CHOOSE_PAYMENT_METHOD

def button_click(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    payment_method = query.data
    query.edit_message_text(text=f'You selected: {payment_method}')
    amount = context.user_data['amount']
    search_binance_api(query, payment_method, amount)
    return ConversationHandler.END

def search_binance_api(query: Update, payment_method: str, amount: str):
    api_key = "GP624XoAEp4kFxpdfH6iQlF5GtKebEMYR81VdArSViw2zYAW6fcQrgJ6fnbJIUIc"
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    payload = {
        "fiat": "MMK",
        "page": 1,
        "rows": 10,
        "tradeType": "SELL",
        "asset": "USDT",
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "filterType": "all",
        "additionalKycVerifyFilter": 0,
        "publisherType": None,
        "payTypes": [payment_method],
        "classifies": ["mass", "profession"],
        "minSingleTransQuantity": amount,  # Include user_input_quantity as a query parameter
    }

    headers = {
        "Content-Type": "application/json",
        "X-Binance-APIKey": api_key
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        display_search_results(query, response)
    except Exception as e:
        print("Error sending request to Binance P2P API:", e)

def display_search_results(query: Update, response: requests.Response):
    if response.status_code != 200:
        query.message.reply_text("Error occurred while fetching data from Binance P2P API.")
        return

    data = response.json()
    advertisements = data.get('data', [])

    if not advertisements:
        query.message.reply_text("No advertisements found.")
        return

    message = "Search results:\n"
    for ad in advertisements:
            adv = ad.get('adv', {})
            advertiser = ad.get('advertiser', {})
            if adv and advertiser:
                adv_payment_methods = [method['identifier'] for method in adv.get('tradeMethods', [])]
                min_trans_quantity_adv = float(adv.get('minSingleTransQuantity', 0))
                max_trans_quantity_adv = float(adv.get('dynamicMaxSingleTransQuantity', 0))
                
                
                if payment_method in adv_payment_methods and \
                    min_trans_quantity_adv <= user_input_quantity <= max_trans_quantity_adv:
                        price = adv.get('price', 'N/A')
                        table_data.append([
                            adv['advNo'],
                            advertiser['nickName'],
                            price,
                            min_trans_quantity_adv,
                            max_trans_quantity_adv
                        ])

    query.message.reply_text(message)

def main() -> None:
    updater = Updater("6953412767:AAGKDKQqLgbOmg3ndzqSPoFgysDcoPbG2Vk")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_AMOUNT: [MessageHandler(Filters.text & ~Filters.command, enter_amount)],
            CHOOSE_PAYMENT_METHOD: [CallbackQueryHandler(button_click)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
