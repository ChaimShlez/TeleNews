FROM python:3.10-slim

WORKDIR /app

COPY services/ManagerMessage/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/ManagerMessage /app/services/ManagerMessage
COPY utils/kafka_pub_sub/pub /app/utils/kafka_pub_sub/pub
COPY utils/kafka_pub_sub/sub /app/utils/kafka_pub_sub/sub
COPY utils/elastic /app/utils/elstic
COPY utils/logger /app/utils/logger
COPY utils/topics /app/utils/topics

CMD ["python", "-m" , "services.ManagerMessage.src.main"]