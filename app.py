from telegram.ext import *
from telegram import *
import telegram
import time
import json


keyee =[["Claim 🎁"],["Balance 💰","Withdraw ✅"]]
markse = ReplyKeyboardMarkup(keyee,one_time_keyboard=True,resize_keyboard=True)

Daily_bonus = 0.25
Mini_Withdraw = 2
bonus = {}
def start(update,context):
    try:
        firstname = update.message.from_user['first_name']
        userid = update.message.chat_id
        user = str(userid)
        data = json.load(open('./users.json', 'r'))
        link = f"<a href='tg://user?id={userid}'>{firstname}</a>"
        msg = f"Hi {link}\nWelcome to Rav Faucet Bot!\nStatus: <code>VIP</code>"
        update.message.reply_text(msg,parse_mode="html",reply_markup=markse,disable_web_page_preview=True)
        if user not in data['balance']:
            data['balance'][user] = 0
            
            
        json.dump(data, open('./users.json', 'w'))
        
    except telegram.error.BadRequest:
        firstname = update.message.from_user['first_name']
        userid = update.message.chat_id
        user = str(userid)
        msg = f"Hi [{firstname}](tg://user?id={userid})\nWelcome to Rav Faucet Bot!\nStatus: VIP"
        update.message.reply_text(msg,parse_mode="markdown",reply_markup=markse,disable_web_page_preview=True)
        if user not in data['balance']:
            data['balance'][user] = 0
            
        json.dump(data, open('./users.json', 'w'))
        
        
def balance(update,context):
    userid = update.message.chat_id
    user =str(userid)
    nm = json.load(open('./users.json', 'r'))
    firstname = update.message.from_user['first_name']

    balance = nm['balance'][user]
    #print(balance)
    msg = f"*Account Balance\nUser: {firstname}\nUser Id:* `{user}`\n*Balance: {balance} TRX* "
    update.message.reply_text(msg,parse_mode="markdown")
    
    
def bonuss(update,context):
    user_id = update.message.chat_id
    user = str(user_id)
    cur_time = int((time.time()))
    data = json.load(open('./users.json', 'r'))
        #bot.send_message(user_id, "*🎁 Bonus Button is Under Maintainance*", parse_mode="Markdown")
    if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 24*60*60):
        data['balance'][(user)] += Daily_bonus
        context.bot.send_message(
            user_id, f"Nice! Your claimed 0.25 TRX Today!\nBe back tommorrow")
        bonus[user_id] = cur_time
        json.dump(data, open('./users.json', 'w'))
    else:
        context.bot.send_message(
                user_id, "You can only take bonus once every 24 hours!",parse_mode="markdown")
        return
    
def withy(update,context):
    user_id = update.message.chat_id
    msg = "For a successful withdrawal\nYou must have upto 2TRX balance\nHow to withdraw\n/withdraw < Amount > < username>\n`/withdraw 10 @RAV`"
    update.message.reply_text(msg,parse_mode="markdown")
    
def withdraw(update,context):
    id = update.message.chat_id
    text = update.message.text.split()
    user = str(id)
    if len(text) == 3:
        amount = text[1]
        wallet = text[2]
        try:
            ye = int(amount)
            if user not in data['balance']:
                data['balance'][user] = 0
            json.dump(data, open('./users.json', 'w'))
            bal = data['balance'][user]
            if bal >= Mini_Withdraw:
                if int(ye) < Mini_Withdraw:
                    update.message.reply_text("Minimum withdraw is 2TRX")
                    return
                if int(ye) > bal:
                    update.message.reply_text("You can't withdraw more than your balance")
                    return 
                
                amo = int(amount)
                data['balance'][user] -= int(amount)
                json.dump(data, open('./users.json', 'w'))
                update.message.reply_text(f"✅ Withdraw Request Processing\nPayments will arrive within 24hours\n\nWithdrawal Details\n{amount} TRX To\n{wallet}")
                context.bot.send_message(chat_id=
                "1185692914", text=f"New Pending Payment\nUserid: `{id}`\nAmount: {amount} TRX\nUsername: `{wallet}`",parse_mode="markdown")
            else:
                update.effective_message.reply_text("Your balance is low to make withdraw")
               
        except ValueError:
            update.effective_message.reply_text("Usage\n/withdraw < amount > < username >")
    else:
        update.message.reply_text("Usage for withdraw\n/withdraw 10 @RAV")
        return
    
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token
    print("STARTING BOT NOW")
    updater = Updater("2068777860:AAEWAWem_DtvgvGsm5YC5TS6v4SQ0FW6vbo")
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('balance', balance))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Balance 💰'),balance))
    updater.dispatcher.add_handler(CommandHandler('bonus', bonuss))
    updater.dispatcher.add_handler(CommandHandler('withdraw', withdraw))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Claim 🎁'),bonuss))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Withdraw ✅'),withy))

   
    
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
if __name__ == '__main__':
    main()