if [ ! -d "_site-packages" ]; then
  docker run -d --name=mypyapp manologcode/text_to_mp3 /bin/ash
  sleep 2
  docker cp mypyapp:/usr/local/lib/python3.10/site-packages ./_site-packages
  docker rm -f mypyapp
fi

docker run -it --rm \
--name=mypyapp \
-e FLASK_APP=app.py \
-e FLASK_ENV=development \
-p 5000:5000 \
-v $PWD/_site-packages:/usr/local/lib/python3.10/site-packages \
-v $PWD/app:/app \
-v $PWD/text_audios:/text_audios \
manologcode/text_to_mp3 \
/bin/ash
