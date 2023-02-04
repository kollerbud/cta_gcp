FROM python:3.8

WORKDIR /src
ENV PORT 8080

COPY requirements.txt .
COPY *.json .

run pip install -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/main.py"]