from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater,Dispatcher, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,CallbackContext
from db import DB
from card import Cart

db = DB('db.json')
cr = Cart('data.json')

def start(update:Update,context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    text = 'Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing!'
    keybord = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='🛍 Magazin', callback_data="view_product_data"),InlineKeyboardButton(text='📦 Savatcha', callback_data="viec_cart_data")],
        [InlineKeyboardButton(text="📞 Biz bilan Bog'lanish", callback_data="contact_us_data"),InlineKeyboardButton(text='📝 Biz haqimizda', callback_data="about_us_data")]
    ])
    bot.sendMessage(chat_id,text,reply_markup=keybord)

def magazin(update:Update,context:CallbackContext):
    query = update.callback_query
    bot = context.bot
    brends = db.get_tables()
    keyboard = []
    row = []
    for brend in brends:
        if len(row) != 4:
            btn = InlineKeyboardButton(
            text = brend.capitalize(),
            callback_data=f"brend_{brend}"
            )
            row.append(btn)
        else:
            keyboard.append(row)
            row = []
            btn = InlineKeyboardButton(
            text = brend.capitalize(),
            callback_data=f"brend_{brend}"
            )
            row.append(btn)
    keyboard.append(row)
    
    menu = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([menu])
    keyboard = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id = query.message.chat.id,message_id = query.message.message_id,text="Quyidagi brandlardan birini tanlang!",reply_markup=keyboard)

def get_product(update:Update, context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    data = query.data
    brend = data.split('_')[-1]

    products = db.get_phone_list(brend)
    # create keyboard
    keyboard = [[], []]
    phone_text = f"1-10/{len(products)}\n\n"
    pr_range = 10


    for i,phone in enumerate(products[:pr_range],1):
        phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
        # create button
        btn = InlineKeyboardButton(
            text = str(i),
            callback_data=f"product_{brend}_{phone.doc_id}"
        )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)

    btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'nextleft_{brend}_{pr_range}')
    btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
    btn3 = InlineKeyboardButton(text="❌", callback_data="view_product_data")

    keyboard.append([btn1,btn3,btn2])


    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id = query.message.chat.id,message_id = query.message.message_id,text=phone_text, reply_markup=reply_markup)

def next_product(update, context):
    query = update.callback_query
    bot = context.bot
    data = query.data.split('_')
    text, brend, pr_range = data
    pr_range = int(pr_range)
    products = db.get_phone_list(brend)

    if text == "nextright":

        if len(products) < pr_range:
            pr_range = 1

        print(len(products), pr_range)
        keyboard = [[], []]
        phone_text = f"{pr_range}-{pr_range+10}/{len(products)}\n\n"

        for i, phone in enumerate(products[pr_range:pr_range+10], 1):
            phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
            # create button
            btn = InlineKeyboardButton(
                text = str(i),
                callback_data=f"product_{brend}_{phone.doc_id}"
            )
            if i < 6:
                # 1 2 3 4 5
                keyboard[0].append(btn)
            else:
                # 6 7 8 9 10
                keyboard[1].append(btn)
        pr_range += 10
        btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'nextleft_{brend}_{pr_range}')
        btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
        btn3 = InlineKeyboardButton(text="❌", callback_data="view_product_data")
        keyboard.append([btn1,btn3,btn2])

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(phone_text, reply_markup=reply_markup)

        query.answer("Next")

    elif text == 'nextleft':

        if len(products) < pr_range:
            pr_range = 0

        print(len(products), pr_range)
        keyboard = [[], []]
        phone_text = f"{pr_range}-{pr_range+10}/{len(products)}\n\n"

        for i, phone in enumerate(products[pr_range:pr_range+10], 1):
            phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
            # create button
            btn = InlineKeyboardButton(
                text = str(i),
                callback_data=f"product_{brend}_{phone.doc_id}"
            )
            if i < 6:
                # 1 2 3 4 5
                keyboard[0].append(btn)
            else:
                # 6 7 8 9 10
                keyboard[1].append(btn)
        pr_range += 10
        btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'nextleft_{brend}_{pr_range}')
        btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
        btn3 = InlineKeyboardButton(text="❌", callback_data="view_product_data")
        keyboard.append([btn1,btn3,btn2])

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = query.message.chat.id,message_id = query.message.message_id,text=phone_text, reply_markup=reply_markup)

        query.answer("Back")

def get_phone(update:Update, context):
    bot  = context.bot
    query = update.callback_query
    data = query.data.split('_')
    text, brend, doc_id = data

    phone = db.getPhone(brend, doc_id)
    price = phone['price']
    ram = phone['RAM']
    memory = phone['memory']
    name = phone['name']
    color = phone['color']
    img = phone['img_url']
    text = f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    btn1 = InlineKeyboardButton(text="🛒 Saqlash", callback_data=f'addcard_{brend}_{doc_id}')
    btn2 = InlineKeyboardButton(text="❌", callback_data='delete')
    btn3 = InlineKeyboardButton(text="⬅️", callback_data=f'left_{brend}_{doc_id}')
    btn4 = InlineKeyboardButton(text="➡️", callback_data=f'right_{brend}_{doc_id}')
    keyboard = InlineKeyboardMarkup([
        [btn3,btn2,btn4],
        [btn1]
    ])

    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=keyboard)

def right(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    data,brend,doc_id = query.data.split('_')
    doc_id = int(doc_id) + 1
    phone = db.getPhone(brend, doc_id)
    price = phone['price']
    ram = phone['RAM']
    memory = phone['memory']
    name = phone['name']
    color = phone['color']
    img = phone['img_url']
    text = f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    btn1 = InlineKeyboardButton(text="🛒 Saqlash", callback_data=f'addcard_{brend}_{doc_id}')
    btn2 = InlineKeyboardButton(text="❌", callback_data='delete')
    btn3 = InlineKeyboardButton(text="⬅️", callback_data=f'left_{brend}_{doc_id}')
    btn4 = InlineKeyboardButton(text="➡️", callback_data=f'right_{brend}_{doc_id}')
    keyboard = InlineKeyboardMarkup([
        [btn3,btn2,btn4],
        [btn1]
    ])
    
    bot.delete_message(chat_id = query.from_user.id,message_id = query.message.message_id,)
    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=keyboard)

def left(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    data,brend,doc_id = query.data.split('_')
    doc_id = int(doc_id) - 1
    phone = db.getPhone(brend, doc_id)
    price = phone['price']
    ram = phone['RAM']
    memory = phone['memory']
    name = phone['name']
    color = phone['color']
    img = phone['img_url']
    text = f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    btn1 = InlineKeyboardButton(text="🛒 Saqlash", callback_data=f'addcard_{brend}_{doc_id}')
    btn2 = InlineKeyboardButton(text="❌", callback_data='delete')
    btn3 = InlineKeyboardButton(text="⬅️", callback_data=f'left_{brend}_{doc_id}')
    btn4 = InlineKeyboardButton(text="➡️", callback_data=f'right_{brend}_{doc_id}')
    keyboard = InlineKeyboardMarkup([
        [btn3,btn2,btn4],
        [btn1]
    ])
    
    bot.delete_message(chat_id = query.from_user.id,message_id = query.message.message_id,)
    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=keyboard)

def addCard(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    data,brend,doc_id = query.data.split('_')
    
    cart = cr.add(brend,doc_id,chat_id)


    query.answer("Saqlandi")

def delete(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    
    bot.delete_message(chat_id = query.from_user.id,message_id = query.message.message_id,)

    query.answer("Delete")


def menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='🛍 Magazin', callback_data="view_product_data"),InlineKeyboardButton(text='📦 Savatcha', callback_data="viec_cart_data")],
        [InlineKeyboardButton(text="📞 Biz bilan Bog'lanish", callback_data="contact_us_data"),InlineKeyboardButton(text='📝 Biz haqimizda', callback_data="about_us_data")]
    ])
    query.edit_message_text("Bosh Menu", reply_markup=keyboard)

def add_card(update, context):
    query = update.callback_query
    btn1 = InlineKeyboardButton(text="📦 Savatni ko'rish", callback_data="cart")
    btn2 = InlineKeyboardButton(text='❌ Savatchani tozalash', callback_data="remove")
    keyboard = []
    keyboard.append([btn1,btn2])
    menu = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([menu])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Siz saqlagan telefonlar', reply_markup=reply_markup)

    query.answer("Done")

def get_cart(update:Update,context:CallbackContext):
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    ct = cr.get_cart(chat_id=chat_id)
    num = 1
    text = ''
    if ct:
        for phone in ct:

            phone = db.getPhone(phone['brand'],phone['doc_id'])
            price = phone['price']
            ram = phone['RAM']
            memory = phone['memory']
            name = phone['name']
            color = phone['color']
            text += f"""{num}.
            📲{name}
            🎨{color}
            💾{ram}/{memory}
            💰{price}
            --------------------------
    """     
            num += 1
    else:
         text = "Savat Bo'sh"
        
    btn1 = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="⬅️", callback_data=f'n_cart')]
        ])
    query.edit_message_text(text,reply_markup=btn1)

def next_cart(update,context):
    query = update.callback_query
    btn1 = InlineKeyboardButton(text="📦 Savatni ko'rish", callback_data="cart")
    btn2 = InlineKeyboardButton(text='❌ Savatchani tozalash', callback_data="remove")
    keyboard = []
    keyboard.append([btn1,btn2])
    menu = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([menu])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Siz saqlagan telefonlar', reply_markup=reply_markup)

    query.answer("Done")

def remove_product(update:Update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    cr.remove(chat_id)

    query.answer("O'chirildi")

def about(update: Update, context: CallbackContext):
    query = update.callback_query

    keyboar = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")]
    ])
    bot = context.bot
    query.edit_message_text(
    text=f'Assalom alaykum {query.from_user.first_name} \nXush kelibsiz botimizga 👍',
    reply_markup=keyboar
    )

def contact(update: Update, context: CallbackContext):
    query = update.callback_query

    keyboar = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='📞 Phone number',callback_data='number'),InlineKeyboardButton(text='📧 Email',callback_data='email')],
        [InlineKeyboardButton(text='📍 Location',callback_data='location'),InlineKeyboardButton(text='📌 Address',callback_data='address')],
        # [InlineKeyboardButton(text='📞 Phone number',url='txt')]
        
    ])
    bot = context.bot
    query.edit_message_text(
    text='Assalom alaykum xush kelibsiz botimizga 👍',
    reply_markup=keyboar
    )

def query(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data
    bot = context.bot
    menu = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    if data=='number':
        phone_1 ='+998661234567'
        phone_2 ='+998661234567'
        text = f'Our phone numbers:\n{phone_1}\n{phone_2}'
        query.edit_message_text(text=text,reply_markup=InlineKeyboardMarkup([[menu]]))
    elif data=='email':
        email = 'Our email: smartphone@gmail.com'
        query.edit_message_text(text=email,reply_markup=InlineKeyboardMarkup([[menu]]))
        
    elif data=='address':
        address = 'Our address: Samarkand, Uzbekistan'
        query.edit_message_text(text=address,reply_markup=InlineKeyboardMarkup([[menu]]))

    elif data=='location':
        # 39.644053, 66.973233
    
        lat = 39.644053
        lon = 66.973233
        bot.send_location(chat_id,latitude=lat,longitude=lon,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data='delete')]]))

    query.answer('Hi')