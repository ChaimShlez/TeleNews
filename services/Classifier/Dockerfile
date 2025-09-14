FROM python:3.10-slim

WORKDIR /app

COPY services/Classifier/requirements.txt .

RUN pip install -r requirements.txt

COPY services/Classifier /app/services/Classifier
COPY utils/kafka /app/utils/kafka
COPY utils/elastic /app/utils/elstic
COPY utils/logs /app/utils/logs

CMD ["python", "-m" , "services.Classifier.src.main"]