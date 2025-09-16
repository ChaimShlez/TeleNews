FROM python:3.10-slim

WORKDIR /app

COPY services/CheckerService/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/CheckerService/src app/services/CheckerService/src

COPY utils/logger app/utils/logger


CMD ["python", "-m", "services.CheckerService.src.main"]