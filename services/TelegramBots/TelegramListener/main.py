from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from config import *
from utils.topics.topics import TOPICS
from utils.mongodb.mongodb_service import MongoDBService
TOKEN = TOKEN_BOT

SELECT_TOPICS = 1

# כאן נשמור את ההעדפות של כל משתמש
user_preferences = {}

# הנושאים לבחירה (אפשר לשנות)


# התחלת שיחה
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
            # adding to mongodb
            mongo = MongoDBService(CONNECTION_STRING,DB_NAME)
            mongo.insert_one(COLLECTION_NAME,{str(user_id) :chosen})


        else:
            await update.message.reply_text("לא נבחרו נושאים. תוכל להריץ /start שוב בכל עת.")
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

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
