FROM python:3.10.0rc2-bullseye AS base
COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY src/ .

ENTRYPOINT ["python3","-u", "./bot.py"]

