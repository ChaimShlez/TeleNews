FROM python:3.10-slim

WORKDIR /app

COPY services/TelegramBots/TelegramListener/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/TelegramBots/TelegramListener /app/services/TelegramBots/TelegramListener
COPY utils/elastic /app/utils/elastic
COPY utils/logger /app/utils/logger
COPY utils/topics /app/utils/topics
COPY utils/mongodb /app/utils/mongodb


CMD ["python", "-m" , "services.TelegramBots.TelegramListener.src.main"]