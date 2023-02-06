FROM python:3.8-slim

WORKDIR /src
ENV PORT 8080

COPY requirements.txt .

run pip install -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/main.py"]