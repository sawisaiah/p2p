import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Currency Converter Bot! ကျွန်တော်တို့ဘော့မှကြိုဆိုပါတယ်\n'
                              'To convert USD to MMK, simply send the amount in USD.')

# Define help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('To convert USD to MMK, simply send the amount in USD.\n'
                              'For example, send "10" to convert 10 USD to MMK.')

# Define conversion handler
def convert_usd_to_mmk(update: Update, context: CallbackContext) -> None:
    try:
        amount_usd = float(update.message.text)
        amount_mmk = amount_usd * 3800  # Convert USD to MMK using fixed exchange rate
        update.message.reply_text(f'{amount_usd} USD is approximately {amount_mmk} MMK.')
    except ValueError:
        update.message.reply_text('Invalid input. Please enter a valid number.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("7046977766:AAHHGr13ehhmNEqV6TTxG6Q0bOi-tleF0xE", use_context=True)  # Replace "TOKEN" with your bot token

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register message handler to handle USD to MMK conversion
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_usd_to_mmk))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
