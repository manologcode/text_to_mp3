FROM python:3.10-alpine

RUN apk update \
    && apk add --no-cache gcc python3-dev musl-dev py3-pip

RUN apk add  --no-cache ffmpeg

WORKDIR /app

COPY ./app /app
RUN pip3 install  --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "wsgi:app"]
