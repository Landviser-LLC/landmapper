########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename
import os
from utils.functions_1d import recalculate_table, plot_1d, calculate_pseudo_depth, filter_1d_table, \
    ConstantsFor1dCalculation, generate_1_calculation, concatenate_batch_of_calculations
import uuid

uploads = Blueprint('uploads', __name__)
uploads_dir = "static/uploads/"  # base uploads dir
plots_dir = "static/Images/"


@uploads.route('/upload', methods=['GET', 'POST'], endpoint='uploads_file')
def uploads_file():
    is_hidden_plot_block = 'hidden'
    is_hidden_plot_block_2d = 'hidden'
    if request.method == 'POST':  # if request is post then upload it to uploads path and read it as csv table
        f = request.files.get('file')  # getting uploaded file
        path_to_upload_file = os.path.join(uploads_dir, secure_filename(f.filename))  # creating path to upload
        try:
            f.save(path_to_upload_file)  # saving file to path with uploads
        except PermissionError:
            pass  # todo print that no file are selected
        if request.form.get('VES-type-select') == '1':
            k_dict = ConstantsFor1dCalculation.default_k()
            k_value = 1
            try:
                k_value = k_dict.get(request.form.get('k-mode-select')) if request.form.get(
                    'k-mode-select') != "Custom" else float(request.form.get('k-parameter'))
            except (ValueError, KeyError):
                pass  # todo: find how to alert exception in UI

            ab_modes_dict = ConstantsFor1dCalculation.ab_mode()
            ab_dict = ConstantsFor1dCalculation.ab()
            ab = ab_dict.get('14m')
            ab_mode = 1
            try:
                ab_mode = ab_modes_dict.get(request.form.get('a-mode-select'))
                ab = ConstantsFor1dCalculation.ab().get(request.form.get('a-mode-select'))
                if not ab:
                    ab = list(map(lambda x: float(x.strip()), request.form.get('a-parameter').split(',')))
            except ValueError:
                pass  # todo: find how to alert exception in UI

            result = []
            i = 1
            list_of_df_before_recalc = []
            list_of_df_after_recalc = []
            # todo make elastic from calculations number
            for df in generate_1_calculation(path_to_upload_file, len(ab)):

                if i % 4 == 0:
                    # print()
                    raw_df = concatenate_batch_of_calculations(list_of_df_before_recalc)

                    recalculated_dfs = concatenate_batch_of_calculations(list_of_df_after_recalc)
                    html_of_table_before_recalculating = raw_df.to_html(classes=['table'])
                    html_of_table_after_recalculating = recalculated_dfs.to_html(classes=['table'])

                    path_to_upload_1d_plot = os.path.join(plots_dir, f'{str(uuid.uuid4())}.png')  # 'plot.png')
                    print(recalculated_dfs)
                    plot_1d(recalculated_dfs, path_to_upload_1d_plot)
                    result.append({'html_of_table_before_recalculating': html_of_table_before_recalculating,
                                   'html_of_table_after_recalculating': html_of_table_after_recalculating,
                                   'path_to_upload_1d_plot': path_to_upload_1d_plot
                                   })
                    list_of_df_before_recalc.clear()
                    list_of_df_after_recalc.clear()
                else:
                    filtered_df = filter_1d_table(df, ab_mode, ab, k=k_value)
                    list_of_df_before_recalc.append(filtered_df)
                    # creating html of recalculated table
                    recalculated_df = recalculate_table(filtered_df.__deepcopy__())
                    calculate_pseudo_depth(recalculated_df)
                    list_of_df_after_recalc.append(recalculated_df)
                i += 1
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
