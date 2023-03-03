FROM python:3.8-slim

WORKDIR /src
ENV PORT 8080

COPY requirements.txt .

run pip install -r requirements.txt

COPY ./src ./src

CMD [ "python", "src/main.py"]

# for local docker run
# docker run --env-file=.env
# gcloud builds and push to artifact
# https://cloud.google.com/build/docs/build-push-docker-image