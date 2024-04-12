FROM python:3.11
LABEL authors="Slava$$$"


WORKDIR /app


COPY requirements.txt requirements.txt
COPY . .
RUN apt -y update
RUN apt -y install nano inetutils-ping
RUN pip install --upgrade --no-cache-dir pip
RUN pip install -r requirements.txt

RUN chmod +x run.sh
