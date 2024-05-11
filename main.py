from bottle import route, run, static_file, request, response, hook
from yt_dlp import YoutubeDL
import ffmpeg
import re
import os

@hook('after_request')
def cleanup():
    if hasattr(request, 'file_path'):
        try:
            os.remove(request.file_path)
            os.remove(request.old_file_path)
        except OSError as e:
            print(f"Error: {e.strerror}")

@route('/download')
def index():
    url = request.query.url
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '%(title)s.mp4',
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        old_file_path = ydl.prepare_filename(info_dict)

    file_path = re.sub(r'\.\w+$', '.mp3', old_file_path)
    extension = "mp3"
    stream = ffmpeg.input(old_file_path)
    stream = ffmpeg.output(stream, file_path)
    ffmpeg.run(stream, quiet=True)
    print(f"[info] Successfully converted the file to {extension}")
    
    request.file_path = file_path
    request.old_file_path = old_file_path

    return static_file(file_path, root='.', download=True)

run(host='0.0.0.0', port=8080)
