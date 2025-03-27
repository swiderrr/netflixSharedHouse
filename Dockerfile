FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROME_BIN=/usr/bin/chromium

COPY requirements.txt .
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD [ "python3", "src/main.py" ]
