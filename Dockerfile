FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN apt update && apt install -y libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libgconf-2-4 \
    libxcb-randr0-dev \
    libxcb-xtest0-dev \
    libxcb-xinerama0-dev \
    libxcb-shape0-dev \
    libxcb-xkb-dev
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "src/main.py" ]
