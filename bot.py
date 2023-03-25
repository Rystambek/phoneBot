from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater,Dispatcher, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,CallbackContext
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

TOKEN = '5766174948:AAERI4lwWYzIfSPaLDBE9gWugxMpNAMgmVE'

updater = Updater(token=TOKEN)
dp = updater.dispatcher

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


updater.start_polling()
updater.idle()