FROM python:3.9-slim

WORKDIR /src
ENV PORT=8080

RUN python -m pip install -U pip

COPY requirements.txt .

RUN pip install -U --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/main.py"]

