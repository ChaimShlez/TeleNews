FROM python:3.10-slim

WORKDIR /app

COPY services/DataLoaders/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY services/DataLoaders/TelegramLoader /app/services/DataLoaders/TelegramLoader
COPY services/DataLoaders/TelegramLoader/my_session.session /app/services/DataLoaders/TelegramLoader

COPY utils/kafka_pub_sub/pub /app/utils/kafka_pub_sub/pub
COPY utils/logger /app/utils/logger
COPY utils/elastic /app/utils/elastic
COPY utils/mongodb /app/utils/mongodb
COPY utils/redis /app/utils/redis



CMD ["python", "-m", "services.DataLoaders.TelegramLoader.main"]