#!/usr/bin/python3
# Coded the 05/11/2021 by Mathieu L and kevin L
# API calls for SKS Server
import json
import os

from flask import Flask, request
from werkzeug.utils import secure_filename

from gpg import GPG

app = Flask(__name__)
gpg = GPG()
app.config.from_mapping(
    SECRET_KEY='dev',
    MAX_CONTENT_LENGTH=16 * 1000 * 1000,
    ALLOWED_EXTENSIONS={'gpg', 'pgp', 'txt'},
    UPLOAD_FOLDER="/home/serversks/.gnupg/"
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Call for searching a key
@app.route('/get/<string:keyword>')
def get_key(keyword):  
    return json.dumps(gpg.searchKeys(keyword))

# Call for exporting the server's public key
@app.route('/export')
def export_key():  
    return gpg.exportKey()

# Call for listing all the keys added to the server
@app.route('/list')
def get():  
    return json.dumps(gpg.listKeys())

# Call for adding a new public key to the server
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # print(request.headers.get("Content-Type"))
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            response = gpg.importKeyToServ(path)
            return json.dumps(response)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
