FROM python:3.8-slim

WORKDIR /src
ENV PORT=8080

RUN python -m pip install -U pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/main.py"]

