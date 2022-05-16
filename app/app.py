from flask import Flask, request, render_template
from gtts import gTTS
import os
import unidecode
from threading import Thread

app = Flask(__name__)

def read_text(text, title, album):
    
    file = gTTS(text=text,lang="es", slow = False)
    file.save("temp_files/first.mp3")
    os.system("ffmpeg -i temp_files/first.mp3 -af 'atempo=1.40' temp_files/second.mp3")
    os.remove("temp_files/first.mp3")
    os.system( 'ffmpeg -i temp_files/fondo.mp3 -i temp_files/second.mp3 -filter_complex "[0:a]volume=.20[A];[1:a][A]amerge[out]" -map [out] -c:a pcm_s16le temp_files/second.wav')
    os.remove("temp_files/second.mp3")
    title = unidecode.unidecode(title).replace(" ", "_")
    name_file = f"/text_audios/{title}.mp3"
    os.system( f'ffmpeg -y -i temp_files/second.wav -metadata title="{title}" -metadata artist="TextToAudio" -metadata album="{album}" -af "volume=1.5" {name_file}')    
    os.remove("temp_files/second.wav")
    return name_file

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == "POST":
        data = request.form
        print(data)
        name_file = data['title'] if 'title' in data else None
        text = data['text'] if 'text' in data else None
        album="leidos"
        if name_file and text:
            name_file = unidecode.unidecode(name_file).replace(" ", "_")
            if "/" in name_file:
                parts=name_file.split('/')
                folder=f'/text_audios/'+parts[0]
                album="texto - " + parts[0]
                if not os.path.exists(folder):
                   os.makedirs(folder)
                   os.chown(folder, 1000, 1000)
            background_thread = Thread(target=read_text, kwargs={"text": text, "title": name_file , "album": album})
            background_thread.start()
            # name_file = read_text(text, name_file)
            number_works = len(text.split())
            return render_template('loading.html', message=f"se trata de un texto de {number_works} palabras se va a proceder a crear el archivo",number_works=number_works )
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/loading/', methods = ['GET'])
def loading():
    file_name='temp_files/first.mp3'
    message = "Proceso finalizado"

    if os.path.isfile(file_name):
        size = os.path.getsize(file_name) 
        message = f"Leyendo Texto..., tamaño de archivo: {size/float(1<<20):,.2f} MB"

    file_name='temp_files/second.wav'
    if os.path.isfile(file_name):
        size = os.path.getsize(file_name) 
        message = f"Reprocesando ..., tamaño de archivo: {size/float(1<<20):,.2f} MB"

    file_name='temp_files/second.mp3'
    if os.path.isfile(file_name):
        size = os.path.getsize(file_name) 
        message = f"Finalizando ..., tamaño de archivo: {size/float(1<<20):,.2f} MB"

    return render_template('loading.html', message=message)    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
