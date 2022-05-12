# TEXTO TO MP3

Se trata de sencilla aplicación de entorno servidor con interface web que nos permite pasa de un texto a mp3.
Esta pensada para instalar en una rapsberry y poder disfrutar de servicio en casa. Esta probada en una Raspeberry pi 4

Para correr la aplicación 

crear primero la carpeta de almacenamiento de resultados

    mkdir text_audios


### con docker

docker run --rm \
--name=text_audios \
-p 5000:80 \
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

 Si la corremos en nuestro ordenador una vez arrancado el servido http://localhost:5000 los archivos generados aparecen en la carpeta text_audios.