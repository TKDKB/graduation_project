FROM python:3.11
LABEL authors="Slava$$$"


WORKDIR /app


COPY requirements.txt requirements.txt

RUN apt -y install nano inetutils-ping nmap
RUN pip install --upgrade --no-cache-dir pip && pip install -r requirements.txt  --no-cache-dir

COPY . .
RUN chmod +x run.sh
