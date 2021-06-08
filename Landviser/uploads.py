########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import render_template, request, Blueprint, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.functions_1d import recalculate_table, plot_1d, calculate_pseudo_depth, filter_1d_table, \
    ConstantsFor1dCalculation, generate_1_calculation
import uuid
from flask_login import login_required

uploads = Blueprint('uploads', __name__)
uploads_dir = "static/uploads/"  # base uploads dir
plots_dir = "static/Images/"
csv_dir = "static/csv/"


@uploads.route('/upload', methods=['GET', 'POST'], endpoint='uploads_file')
@login_required
def uploads_file():
    is_hidden_plot_block = 'hidden'
    is_hidden_plot_block_2d = 'hidden'
    if request.method == 'POST':  # if request is post then upload it to uploads path and read it as csv table
        f = request.files.get('file')  # getting uploaded file
        path_to_upload_file = os.path.join(uploads_dir, secure_filename(f.filename))  # creating path to upload
        try:
            f.save(path_to_upload_file)  # saving file to path with uploads
        except PermissionError:
            path_to_upload_file = None
            flash('File not uploaded')
        if request.form.get('VES-type-select') == '1':
            k_dict = ConstantsFor1dCalculation.default_k.value
            k_value = 1
            try:
                k_value = k_dict.get(request.form.get('k-mode-select')) if request.form.get(
                    'k-mode-select') != "Custom" else float(request.form.get('k-parameter'))
            except (ValueError, KeyError):
                flash('K value incorrect by default used K1')

            ab_modes_dict = ConstantsFor1dCalculation.AB_mode.value
            ab_dict = ConstantsFor1dCalculation.AB.value
            ab = ab_dict.get('14m')
            ab_mode = 1
            try:
                ab_mode = ab_modes_dict.get(request.form.get('a-mode-select'))
                ab = ab_dict.get(request.form.get('a-mode-select'))
                if not ab:
                    ab = list(map(lambda x: float(x.strip()), request.form.get('a-parameter').split(',')))
            except ValueError:
                flash('AB values incorrect')

            mn_dict = ConstantsFor1dCalculation.MN.value
            mn = mn_dict.get('14m')
            try:
                mn = mn_dict.get(request.form.get('mn-mode-select'))
                if not mn:
                    mn = list(map(lambda x: float(x.strip()), request.form.get('mn-parameter').split(',')))
            except ValueError:
                flash('MN values incorrect')
            try:
                assert len(ab) == len(mn), "Lengths of MN and AB are not the same"
            except AssertionError as e:
                flash(e.__str__())
            result = []

            for df in generate_1_calculation(path_to_upload_file, len(ab)):
                filtered_df = filter_1d_table(df, ab_mode, ab, k=k_value)
                html_of_table_before_recalculating = filtered_df.to_html(classes=['table'])
                # creating html of recalculated table
                recalculated_df = recalculate_table(filtered_df.__deepcopy__())
                calculate_pseudo_depth(recalculated_df)
                uid = uuid.uuid4()
                recalculated_df.to_csv(os.path.join(csv_dir, f'{uid}.csv'), index=False)
                html_of_table_after_recalculating = recalculated_df.to_html(classes=['table'])

                path_to_upload_1d_plot = os.path.join(plots_dir, f'{str(uid)}.png')
                plot_1d(recalculated_df, path_to_upload_1d_plot)
                result.append({'html_of_table_before_recalculating': html_of_table_before_recalculating,
                               'html_of_table_after_recalculating': html_of_table_after_recalculating,
                               'path_to_upload_1d_plot': path_to_upload_1d_plot,
                               'uid': str(uid)
                               })
            return render_template('upload.html',
                                   result=result,
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


@uploads.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(csv_dir, filename, as_attachment=True)
