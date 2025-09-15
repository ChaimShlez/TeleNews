FROM python:3.10-slim

WORKDIR /app

COPY services/TelegramBots/TelegramListener/requirements.txt .

RUN pip install -r requirements.txt

COPY services/TelegramBots/TelegramListener /app/services/TelegramBots/TelegramListener
COPY utils/elastic /app/utils/elstic
COPY utils/logger /app/utils/logger

CMD ["python", "-m" , "services.TelegramBots.TelegramListener.src.main"]