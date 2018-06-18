#Download base image python 3.5
FROM python:3.5

WORKDIR /receipt_bot


RUN pip install requirements.txt

RUN echo "Asia/Tehran" > /etc/timezone

COPY . /receipt_bot
CMD ["python3.5", "receipt_bot.py"]

