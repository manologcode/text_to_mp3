# TEXTO TO MP3

Se trata de sencilla aplicacion de entorno servidor con interface web que nos permite pasa de un texto a mp3.
esta pensada para instalar en un rapsberry y poder disfrutar de servicio

para correr la aplicacion 

### con docker

docker run --rm \
--name=text_audios \
-p 5000:80
-v $PWD/text_audios:/text_audios \
manologcode/text_to_mp3

### con docker compose

services:
  flaskapp:
    image: manologcode/text_to_mp3
    restart: always
    container_name: text_to_mp3
    command: /usr/local/bin/gunicorn wsgi:app  -w 5 -b :5000 --reload
    ports:
      - "5000:5000"
    volumes:
      - ./text_audios:/text_audios