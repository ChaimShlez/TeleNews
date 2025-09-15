from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from telegram import Bot
from services.TelegramBots.TelegramSend.src.config import *
import uvicorn
import os
import io

TOKEN = TOKEN_BOT
bot = Bot(token=TOKEN)

app = FastAPI()

@app.post("/send")
async def send_message(
    message: str = Form(...),
    users_id: List[str] = Form(...),  
    file: UploadFile = File(None)

):
    
    if len(users_id) == 1 and "," in users_id[0]:
        users_id = [x.strip() for x in users_id[0].split(",")]
    
    

    async def send_one(user_id):
        try:
            file_bytes = await file.read() if file else None
            if file_bytes:
                filename = file.filename
                ext = os.path.splitext(filename)[1].lower()
                print(ext)

                # יוצרים BytesIO עם שם קובץ
                file_obj = io.BytesIO(file_bytes)
                file_obj.name = filename  # חשוב! השם המקורי

                if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    await bot.send_photo(chat_id=int(user_id), photo=file_obj, caption=message)
                elif ext in ['.pdf', '.zip', '.docx', '.txt']:
                    await bot.send_document(chat_id=int(user_id), document=file_obj, caption=message)
                elif ext in ['.mp3', '.wav']:
                    await bot.send_audio(chat_id=int(user_id), audio=file_obj, caption=message)
                elif ext in ['.mp4']:
                    await bot.send_video(chat_id=int(user_id), video=file_obj, caption=message)
                else:
                    await bot.send_document(chat_id=int(user_id), document=file_obj, caption=message)
            else:
                await bot.send_message(chat_id=int(user_id), text=message)

        except Exception as e:
            print(f"שליחה נכשלה ל-{user_id}: {e}")

    # שליחה במקביל (אם יש הרבה משתמשים)
    
    import asyncio
    await asyncio.gather(*(send_one(uid) for uid in users_id) ,return_exceptions=True)

    return {"status": "sent", "count": len(users_id)}


if __name__ == "__main__":
   
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)