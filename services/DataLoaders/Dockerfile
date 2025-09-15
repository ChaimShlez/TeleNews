FROM python:3.10-slim

WORKDIR /app

COPY services/DataLoaders/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/DataLoaders/TelegramLoader app/services/DataLoaders/TelegramLoader
COPY utils/kafka_pub_sub/pub app/utils/kafka_pub_sub/pub
COPY utils/logger app/utils/logger
COPY utils/elastic app/utils/elastic
COPY utils/mongodb app/utils/mongodb

CMD ["python", "-m", "services.DataLoaders.TelegramLoader.main"]