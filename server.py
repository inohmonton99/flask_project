# http://flask.pocoo.org/docs/patterns/fileuploads/
import os
from flask import Flask, request

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            print(f'file {filename} accepted')
            # TODO: login with onepanel cli using token
            # TODO: establish connection to onepanel workspace
            # TODO: upload file with SDK
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '''
            <!doctype html>
                <h1> File Uploaded </h1>
                <a href="/" class="previous">&laquo; Previous</a>
            '''
        else:
            print(f'{file.filename} is not a video file!')

    return '''
    <!doctype html>
    <title>Video Uploader</title>
    <h1>Video Uploader</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
