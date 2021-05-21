from flask import Flask, render_template, request, Blueprint
from werkzeug.utils import secure_filename

uploads = Blueprint('uploads', __name__)


@uploads.route('/upload', endpoint='upload_file')
def upload_file():
    return render_template('upload.html')


@uploads.route('/uploader', methods=['GET', 'POST'], endpoint='uploads_file')
def uploads_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
