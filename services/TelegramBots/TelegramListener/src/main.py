from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from services.TelegramBots.TelegramListener.src.config import *
from utils.topics.topics import TOPICS
from utils.mongodb.mongodb_service import MongoDBService

TOKEN = TOKEN_BOT
SELECT_CHANNEL = 2
SELECT_TOPICS = 1

mongo = MongoDBService(CONNECTION_STRING, DB_NAME)
# כאן נשמור את ההעדפות של כל משתמש
user_preferences = {}




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message is not None)  :
        user_id = update.message.from_user.id
        # רושמים את המשתמש אם עוד לא נרשם
        if user_id not in user_preferences:
            user_preferences[user_id] = set()
        # מציגים אפשרויות נושאים
        keyboard = [[topic] for topic in TOPICS.keys()]
        await update.message.reply_text(
            "באיזה נושאים אתה רוצה לקבל עדכונים? בחר אחד כל פעם, או כתוב /done כשסיימת.",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return SELECT_TOPICS

# בחירת נושא (הוספה להעדפה)
async def select_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message is not None)  :
        user_id = update.message.from_user.id
        topic = update.message.text
        if topic in TOPICS.keys():
            user_preferences[user_id].add(TOPICS[topic])
            await update.message.reply_text(f"הוספת את הנושא: {topic}. תוכל לבחור עוד נושא, או /done כדי לסיים.")
        else:
            await update.message.reply_text("הנושא לא מוכר, נסה לבחור מרשימת הכפתורים.")
        return SELECT_TOPICS

# סיום בחירת נושאים
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (update.message is not None)  :
        user_id = update.message.from_user.id
        print(user_id)
        chosen = user_preferences.get(user_id, set())
        if chosen:
            await update.message.reply_text(f"נרשמת לנושאים: {', '.join(chosen)}")
            try:
                # adding to mongodb
                mongo.insert_one(COLLECTION_NAME,{"user_id":str(user_id),"topics" :list(chosen)})
            except Exception as e:
                print(f"mongo error: {e}")
                await update.message.reply_text("אירעה שגיאה בשמירת הנושאים. נסה שוב מאוחר יותר.")


        else:
            await update.message.reply_text("לא נבחרו נושאים. תוכל להריץ /start שוב בכל עת.")
        return ConversationHandler.END
    

async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        await update.message.reply_text("אנא כתוב את קישור הערוץ שברצונך לשמור (לדוג' https://t.me/TeleNews1_bot):")
        return SELECT_CHANNEL  # נעבור לשלב קליטת הערוץ

async def receive_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        user_id = update.message.from_user.id
        channel = update.message.text.strip()
        try:
            mongo.insert_one( CHANNEL_COLLECTION_NAME, {"user_id": str(user_id) , "link":channel })
            await update.message.reply_text(f"הערוץ {channel} נשמר בהצלחה! 🙏")
        except Exception as e:
            print(f"mongo error: {e}")
            await update.message.reply_text("אירעה שגיאה בשמירת הערוץ. נסה שוב מאוחר יותר.")
        return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_TOPICS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, select_topic),
                CommandHandler('done', done)
            ]
        },
        fallbacks=[CommandHandler('done', done)]
    )

    channel_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('channel', channel_command)],
    states={
        SELECT_CHANNEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_channel),
        ],
    },
    fallbacks=[],
)

    app.add_handler(channel_conv_handler)
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
