import telebot
from telebot import types
import pygments
from pygments import lexers, formatters
from io import BytesIO
import os

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')  # Fetch token from environment variables
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "Welcome to the Code Highlighter Bot!\n\n"
        "This bot highlights code in various programming languages.\n\n"
        "Simply send me a piece of code, and I'll format it for you.\n\n"
        "Commands:\n"
        "/help - Display this help message"
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "To use this bot, just send me the code you want to highlight.\n"
        "I will return the formatted code with syntax highlighting.\n\n"
        "Supported languages include Python, JavaScript, HTML, and more.\n"
        "For a full list of supported languages, you can refer to the Pygments documentation."
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def highlight_code(message):
    code = message.text.strip()
    if not code:
        bot.send_message(message.chat.id, "Please send me some code to highlight.")
        return
    
    # Detect language from the message or use a default one
    lexer = lexers.get_lexer_by_name('python', fallback=lexers.TextLexer())
    formatter = formatters.HtmlFormatter(style='colorful')
    
    # Highlight the code
    highlighted_code = pygments.highlight(code, lexer, formatter)
    
    # Send highlighted code back to the user
    with BytesIO(highlighted_code.encode('utf-8')) as bio:
        bio.name = 'highlighted_code.html'
        bot.send_document(message.chat.id, bio, caption='Here is your highlighted code.')

bot.polling()
