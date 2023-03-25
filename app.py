from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,Dispatcher
from telegram import Update,Bot
from handler import (start,
                     magazin,
                     get_product,
                     next_product,
                     get_phone,
                     menu,
                     add_card,
                     remove_product,
                     addCard,
                     get_cart,
                     next_cart,
                     about,
                     contact,
                     query,
                     delete
                     )
from flask import Flask, request
import os

# get token from environment variable
TOKEN = '5766174948:AAERI4lwWYzIfSPaLDBE9gWugxMpNAMgmVE'

bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/webhook', methods=["POST", "GET"])
def hello():
    if request.method == 'GET':
        return 'hi from Python2022I'
    elif request.method == "POST":
        data = request.get_json(force = True)
        
        dp: Dispatcher = Dispatcher(bot, update_queue=None, workers=0)
        update:Update = Update.de_json(data, bot)
    
        #update 
                
        dp.add_handler(CommandHandler("start",start))
        dp.add_handler(CallbackQueryHandler(magazin,pattern='view_product_data'))
        dp.add_handler(CallbackQueryHandler(get_product,pattern='brend'))
        dp.add_handler(CallbackQueryHandler(next_product, pattern="next"))
        dp.add_handler(CallbackQueryHandler(get_phone, pattern="product"))
        dp.add_handler(CallbackQueryHandler(menu, pattern="bosh_menu"))
        dp.add_handler(CallbackQueryHandler(addCard, pattern="addcard"))
        dp.add_handler(CallbackQueryHandler(add_card, pattern="viec_cart_data"))
        dp.add_handler(CallbackQueryHandler(get_cart, pattern="cart"))
        dp.add_handler(CallbackQueryHandler(next_cart, pattern="n_cart"))
        dp.add_handler(CallbackQueryHandler(remove_product, pattern="remove"))
        dp.add_handler(CallbackQueryHandler(about,pattern='about_us_data'))
        dp.add_handler(CallbackQueryHandler(contact,pattern='contact_us_data'))
        dp.add_handler(CallbackQueryHandler(delete,pattern='delete'))
        dp.add_handler(CallbackQueryHandler(query))


        
        dp.process_update(update)
        return 'ok'