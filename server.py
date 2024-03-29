# http://flask.pocoo.org/docs/patterns/fileuploads/
import os

from flask import Flask, flash, request, redirect, url_for, render_template
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'

if UPLOAD_FOLDER not in os.getcwd():
    os.makedirs('uploads', exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}

app = Flask(__name__)
api = Api(app)
app.secret_key = "secret_key_54321"
# directory to save uploaded videos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# config to set maximum file size(current = 16mb)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
file_curl = {}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class TodoSimple(Resource):
    # input filename to upload
    def put(self, file):
        file_curl[file] = request.form['filename']
        return file_curl[file]

    # process uploading for filename
    def get(self, file):
        filename = file_curl[file]
        filename_dir = os.path.abspath(filename)
        if os.path.isfile(filename):
            if file and allowed_file(filename):
                filename = secure_filename(filename_dir)
                # TODO: need to convert string file to file object
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                except AttributeError:
                    return "file type not accepted"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # for local UI uploading
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file path for uploads
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
    return '''
    <!doctype html>
        <title>Upload new File</title>
        <h1>File Successfully Uploaded</h1>
        <a href="/" class="previous">Previous</a>      
    '''


@app.errorhandler(404)
def not_found(error):
    return render_template('/static/error.html'), 404


api.add_resource(TodoSimple, '/<file>')

if __name__ == '__main__':
    app.run(debug=True)
