import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Simple Calculator Bot!\n'
                              'Please use /help to see available commands.')

# Define help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Available commands:\n'
                              '/start - Start the bot\n'
                              '/help - Display help message\n'
                              '/add <num1> <num2> - Add two numbers\n'
                              '/subtract <num1> <num2> - Subtract num2 from num1\n'
                              '/multiply <num1> <num2> - Multiply two numbers\n'
                              '/divide <num1> <num2> - Divide num1 by num2\n')

# Define arithmetic operation handlers
def add(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) != 2:
        update.message.reply_text('Usage: /add <num1> <num2>')
        return
    try:
        num1 = float(args[0])
        num2 = float(args[1])
        result = num1 + num2
        update.message.reply_text(f'Result: {result}')
    except ValueError:
        update.message.reply_text('Invalid input. Please enter valid numbers.')

def subtract(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) != 2:
        update.message.reply_text('Usage: /subtract <num1> <num2>')
        return
    try:
        num1 = float(args[0])
        num2 = float(args[1])
        result = num1 - num2
        update.message.reply_text(f'Result: {result}')
    except ValueError:
        update.message.reply_text('Invalid input. Please enter valid numbers.')

def multiply(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) != 2:
        update.message.reply_text('Usage: /multiply <num1> <num2>')
        return
    try:
        num1 = float(args[0])
        num2 = float(args[1])
        result = num1 * num2
        update.message.reply_text(f'Result: {result}')
    except ValueError:
        update.message.reply_text('Invalid input. Please enter valid numbers.')

def divide(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) != 2:
        update.message.reply_text('Usage: /divide <num1> <num2>')
        return
    try:
        num1 = float(args[0])
        num2 = float(args[1])
        if num2 == 0:
            update.message.reply_text('Cannot divide by zero.')
            return
        result = num1 / num2
        update.message.reply_text(f'Result: {result}')
    except ValueError:
        update.message.reply_text('Invalid input. Please enter valid numbers.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater("6953412767:AAGKDKQqLgbOmg3ndzqSPoFgysDcoPbG2Vk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("subtract", subtract))
    dispatcher.add_handler(CommandHandler("multiply", multiply))
    dispatcher.add_handler(CommandHandler("divide", divide))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()


