########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Flask, render_template, request, Blueprint
from werkzeug.utils import secure_filename
import pandas as pd
import os
from utils.functions_1d import recalculate_table

uploads = Blueprint('uploads', __name__)
uploads_dir = "uploads\\"  # base uploads dir


@uploads.route('/upload', methods=['GET', 'POST'], endpoint='uploads_file')
def uploads_file():
    if request.method == 'POST':  # if request is post then upload it to uploads path and read it as csv table
        f = request.files.get('file')  # getting uploaded file
        path_to_upload = os.path.join(uploads_dir, secure_filename(f.filename))  # creating path to upload
        f.save(path_to_upload)  # saving file to path with uploads
        df = pd.read_csv(path_to_upload)
        html_of_table_before_recalculating = df.to_html()
        html_of_table_after_recalculating = recalculate_table(df).to_html()  # creating html of recalculated table
        return render_template('upload.html', table_before=html_of_table_before_recalculating,
                               table_after=html_of_table_after_recalculating,
                               table_title_before="The source table is:<br>",
                               table_title_after="The recalculated table is:<br>")
    return render_template('upload.html')  # if request get than nothing to do
