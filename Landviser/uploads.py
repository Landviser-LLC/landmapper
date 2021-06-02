########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename
import pandas as pd
import os
from utils.functions_1d import recalculate_table, plot_1d, calculate_pseudo_depth

uploads = Blueprint('uploads', __name__)
uploads_dir = "static/uploads\\"  # base uploads dir
plots_dir = "static/Images\\"


@uploads.route('/upload', methods=['GET', 'POST'], endpoint='uploads_file')
def uploads_file():
    # print('UPLOADS1D')
    is_hidden_plot_block = 'hidden'
    is_hidden_plot_block_2d = 'hidden'
    if request.method == 'POST':  # if request is post then upload it to uploads path and read it as csv table

        f = request.files.get('file')  # getting uploaded file
        path_to_upload_file = os.path.join(uploads_dir, secure_filename(f.filename))  # creating path to upload
        f.save(path_to_upload_file)  # saving file to path with uploads
        if request.form.get('VES-type-select') == '1':
            df = pd.read_csv(path_to_upload_file)

            html_of_table_before_recalculating = df.to_html(classes=['table'])
            html_of_table_after_recalculating = recalculate_table(df).to_html(
                classes=['table'])  # creating html of recalculated table
            path_to_upload_1d_plot = os.path.join(plots_dir, 'plot.png')

            calculate_pseudo_depth(df)
            plot_1d(df, path_to_upload_1d_plot)

            # is_hidden_plot_block = 'visible'
            return render_template('upload.html',
                                   table_before=html_of_table_before_recalculating,
                                   table_after=html_of_table_after_recalculating,
                                   table_title_before="The source table is:<br>",
                                   table_title_after="The recalculated table is:<br>",
                                   plot_name='Plot for',
                                   plot_path=path_to_upload_1d_plot,
                                   is_hidden_plot_block='visible',
                                   is_hidden_plot_block_2d=is_hidden_plot_block_2d)
        elif request.form.get('VES-type-select') == '2':
            pass
            # show_2d(path_to_upload_file, os.path.join(plots_dir, '2d-plot.png'))
            # return render_template('upload.html',
            #                       is_hidden_plot_block_2d='visible',
            #                       is_hidden_plot_block=is_hidden_plot_block,
            #                       plot_path_2d=os.path.join(plots_dir, '2d-plot.png')
            #                       )
    return render_template('upload.html',
                           is_hidden_plot_block=is_hidden_plot_block,
                           is_hidden_plot_block_2d=is_hidden_plot_block_2d)  # if request get than nothing to do
