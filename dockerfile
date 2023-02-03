FROM python:3.8

WORKDIR /src

COPY requirements.txt .
COPY *.json .

run pip install -r requirements.txt

COPY ./src ./src

CMD [ "python", "./src/data_to_bq.py"]