FROM python:3.10-slim

WORKDIR /app

COPY services/Translator/requirements.txt .

RUN pip install -r requirements.txt

COPY services/Translator /app/services/Translator
COPY utils/kafka_pub_sub /app/utils/kafka_pub_sub
COPY utils/elastic /app/utils/elstic
COPY utils/logger /app/utils/logger

CMD ["python", "-m" , "services.Translator.src.main"]