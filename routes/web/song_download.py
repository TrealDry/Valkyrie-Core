from . import web
from os.path import join
from config import PATH_TO_ROOT
from flask import send_from_directory


@web.route("/song/<path:filename>", methods=['POST', 'GET'])
def song_download(filename):
    directory = join(PATH_TO_ROOT, "data", "song")
    return send_from_directory(directory=directory, path=filename)
