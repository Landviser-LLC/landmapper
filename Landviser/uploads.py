########################################################################################
######################          Import packages      ###################################
########################################################################################
import os
import uuid

import pandas as pd
from flask import render_template, request, Blueprint, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required

from utils.functions_2d import parse_web_request_2d, filter_2d_df, read_2d_file, save_to_dat, concatenate_all_files
from utils.functions_1d import recalculate_table, plot_1d, calculate_pseudo_depth, filter_1d_table, \
    ConstantsFor1dCalculation, generate_1_calculation, concatenate_all_dataframes

uploads = Blueprint('uploads', __name__)
uploads_dir = "static/uploads/"  # base uploads dir
plots_dir = "static/Images/"
csv_dir = "static/csv/"


def delete_raw_files(file_list):
    for path in file_list:
        os.remove(path)


@uploads.route('/upload', methods=['GET', 'POST'], endpoint='uploads_file')
@login_required
def uploads_file():
    is_hidden_plot_block = 'hidden'
    is_hidden_plot_block_2d = 'hidden'
    if request.method == 'POST':  # if request is post then upload it to uploads path and read it as csv table
        is_hidden_plot_block = 'visible'
        files = request.files.getlist('file')  # getting uploaded file
        path_list = []
        try:
            # Claiming all files and saving them
            for file in files:
                path_to_upload_file = os.path.join(uploads_dir,
                                                   secure_filename(file.filename))  # creating path to upload
                path_list.append(path_to_upload_file)
                file.save(path_to_upload_file)  # saving file to path with uploads
            uid = uuid.uuid4()
            path_to_save = os.path.join(uploads_dir, f"{uid}.csv")
            concatenate_all_files(path_list, path_to_save)
        except PermissionError:
            path_to_save = None
            flash('File not uploaded')
            is_hidden_plot_block = 'hidden'
        finally:
            # Deleting all claimed from user files
            delete_raw_files(path_list)

        if request.form.get('VES-type-select') == '1':
            # Receiving data from user block
            k_dict = ConstantsFor1dCalculation.default_k.value
            k_value = 1
            try:
                k_value = k_dict.get(request.form.get('k-mode-select')) if request.form.get(
                    'k-mode-select') != "Custom" else float(request.form.get('k-parameter'))
            except (ValueError, KeyError):
                flash('K value incorrect by default used K1')
                is_hidden_plot_block = 'hidden'

            ab_modes_dict = ConstantsFor1dCalculation.AB_mode.value
            ab_dict = ConstantsFor1dCalculation.AB.value
            ab = ab_dict.get('14m')
            ab_mode = 1
            try:
                ab_mode = ab_modes_dict.get(request.form.get('a-mode-select'))
                ab = ab_dict.get(request.form.get('a-mode-select'))
                if ab_mode == 4:
                    ab = [float(val) for val in request.form.getlist('ab-input')]
            except ValueError:
                flash('AB values incorrect')
                is_hidden_plot_block = 'hidden'

            mn_dict = ConstantsFor1dCalculation.MN.value
            mn = mn_dict.get('14m')
            try:
                mn = mn_dict.get(request.form.get('mn-mode-select'))
                if ab_mode == 4:
                    mn = [float(val) for val in request.form.getlist('mn-input')]
            except ValueError:
                flash('MN values incorrect')
                is_hidden_plot_block = 'hidden'
            try:
                assert len(ab) == len(mn), "Lengths of MN and AB are not the same"

            except AssertionError as e:
                is_hidden_plot_block = 'hidden'
                flash(e.__str__())
            # End of receiving block
            result = []
            list_of_dataframes = []
            # Splitting dataframes
            for i, df in enumerate(generate_1_calculation(path_to_save, len(ab))):
                filtered_df = filter_1d_table(df, mode=ab_mode, AB_values=ab, MN_values=mn, k=k_value)
                # creating html of recalculated table
                recalculated_df = recalculate_table(filtered_df.__deepcopy__())
                calculate_pseudo_depth(recalculated_df)
                list_of_dataframes.append(recalculated_df)
                uid = uuid.uuid4()
                path_to_upload_1d_plot = os.path.join(plots_dir, f'{str(uid)}.png')
                plot_1d(recalculated_df, path_to_upload_1d_plot, i)
                result.append({'path_to_upload_1d_plot': path_to_upload_1d_plot,
                               'uid': str(uid)
                               })
            final_df = pd.DataFrame()
            try:
                final_df = concatenate_all_dataframes(list_of_dataframes)
                classes = ['table']
            except IndexError:
                classes = ['hidden-table']
                flash("Unparseble fields exists")
            uid = uuid.uuid4()
            final_df.to_csv(os.path.join(csv_dir, f'{uid}.csv'), index=False)
            final_df_html = final_df.to_html(classes=classes)
            return render_template('upload.html',
                                   result=result,
                                   uid=str(uid),
                                   final_df=final_df_html,
                                   is_hidden_plot_block=is_hidden_plot_block,
                                   is_hidden_plot_block_2d=is_hidden_plot_block_2d
                                   )
        elif request.form.get('VES-type-select') == '2':
            # Receiving data from user
            try:
                layers_number = int(request.form.get('layers_number'))
                file_name = request.form.get('file_name')
            except ValueError:
                flash('Incorrect layers number value')
            try:
                first_plug_numbers = [int(x) for x in request.form.getlist('first_plug_number')]
                end_plug_numbers = [int(x) for x in request.form.getlist('end_plug_number')]
                step = [float(x) for x in request.form.getlist('step')]
                dipole_distance = [float(x) for x in request.form.getlist('dipole_distance')]
                measurements_number = [int(x) for x in request.form.getlist('measurment_number_input')]
                first_points_for_measurements = [float(x) for x in request.form.getlist('first_measurement_point_input')]
            except ValueError:
                flash('Incorrect layers filling')
            else:
                # todo: K сеты для 1D
                try:
                    # Parsing user information into layers
                    layers = parse_web_request_2d(layers_number, step, dipole_distance, measurements_number,
                                                  first_plug_numbers,
                                                  end_plug_numbers, first_points_for_measurements)
                except IndexError:
                    flash("More layers than needed.")
                df = read_2d_file(path_to_save)
                uid = uuid.uuid4()
                result_df = filter_2d_df(df, layers)
                save_to_dat(result_df, os.path.join(csv_dir, f'{uid}.dat'), file_name)
                is_hidden_plot_block = 'hidden'
                final_df_html = result_df.to_html(classes=['table'])
                is_hidden_plot_block_2d = 'visible'
                return render_template('upload.html',
                                       uid=str(uid),
                                       final_df_2d=final_df_html,
                                       is_hidden_plot_block=is_hidden_plot_block,
                                       is_hidden_plot_block_2d=is_hidden_plot_block_2d
                                       )

    return render_template('upload.html',
                           is_hidden_plot_block=is_hidden_plot_block,
                           is_hidden_plot_block_2d=is_hidden_plot_block_2d,
                           uid='',
                           final_df=None)  # if request get than nothing to do


@uploads.route('/download_csv/<path:filename>')
def download_csv(filename):
    """This function used as api for downloading csv files generated by 1D calculation"""
    return send_from_directory(csv_dir, filename, as_attachment=True)


@uploads.route('/download_dat/<path:filename>')
def download_dat(filename):
    """This function used as api for downloading dat file generated by 2D calculation"""
    return send_from_directory(csv_dir, filename, as_attachment=True)
