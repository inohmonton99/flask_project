# http://flask.pocoo.org/docs/patterns/fileuploads/
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

if UPLOAD_FOLDER not in os.getcwd():
    os.makedirs('uploads', exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}

app = Flask(__name__)
app.secret_key = "secret_key_54321"
# directory to save uploaded videos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# config to set maximum file size(current = 16mb)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
