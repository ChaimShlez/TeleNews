FROM python:3.10-slim

WORKDIR /app

COPY services/TelegramBots/TelegramSend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/TelegramBots/TelegramSend /app/services/TelegramBots/TelegramSend
COPY utils/elastic /app/utils/elastic
COPY utils/logger /app/utils/logger
COPY utils/topics /app/utils/topics

CMD ["python", "-m" , "services.TelegramBots.TelegramSend.src.main"]