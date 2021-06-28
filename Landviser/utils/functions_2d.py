import math

import pandas as pd
import numpy as np
from flask import flash


class Layer:
    def __init__(self, measurements_number, step, dipole_distance, first_plug_position, end_plug_position,
                 first_point_for_measurement):
        self.__measurements_number = measurements_number
        self.__step = step
        self.__dipole_distance = dipole_distance
        self.__first_plug_position = first_plug_position
        self.__end_plug_position = end_plug_position
        self.__first_point_for_measurement = first_point_for_measurement
        self.__layer = dict()
        self.__start_points = self.__create_start_points()

        self.__create_measurements()
        # print(self.layer)

    @property
    def layer(self):
        return self.__layer

    def __create_start_points(self):
        return np.arange(self.__first_plug_position * self.__step,
                         self.__end_plug_position * self.__step,
                         self.__step
                         ).tolist()

    def __create_measurements(self):
        for start_point in self.__start_points:
            self.__layer[(start_point, start_point + self.__dipole_distance)] = self.__create_one_measurement(
                start_point, self.__measurements_number)

    def __create_one_measurement(self, start_point, measurement_number):
        print(start_point, self.__first_point_for_measurement, self.__step, self.__dipole_distance)
        return [(self.__first_point_for_measurement + start_point + i * self.__step,
                 self.__first_point_for_measurement + start_point + self.__dipole_distance + i * self.__step)
                for i in range(int(measurement_number))]  # here can be bug

    def to_df(self):
        """In this method will be created dataframe representation of layer"""
        df_dict = {'A': [], 'B': [], 'M': [], 'N': []}
        for key, val in self.__layer.items():
            for mn in val:
                df_dict['A'].append(key[0])
                df_dict['B'].append(key[1])
                df_dict['M'].append(mn[0])
                df_dict['N'].append(mn[1])
        return pd.DataFrame(df_dict)

    def __str__(self):
        return self.__layer.__str__()


def concatenate_all_files(files, path_to_save):
    """In this function will be concatenated dataframes received from form into one huge dataframe"""
    dataframe_list = []
    for file in files:
        dataframe_list.append(pd.read_csv(file))
    df = pd.concat(dataframe_list, ignore_index=True)
    df.to_csv(path_to_save, index=False)


def is_allowable_measurements_number(measurements_number, dipole_distance):
    """In this function will be checked currency of measurements number"""
    return measurements_number <= dipole_distance * 7


def is_allowable_first_plug_position(first_plug_position, minimal_allowable_first_plug_position):
    return first_plug_position > minimal_allowable_first_plug_position


def parse_web_request_2d(layers_number, step, dipole_distances, measurements_number, first_plug_position,
                         end_plug_position, first_points_for_measurements):
    """In this function will be parsed data claimed from form and generates layers objects"""
    layers = []
    for i in range(layers_number):

        used_measurements_number = measurements_number[i]
        used_first_plug_position = first_plug_position[i]
        if not is_allowable_measurements_number(measurements_number[i], dipole_distances[i]):
            # If value of measurements number more than available than
            used_measurements_number = dipole_distances[i] * 7
            flash(f"Measurements number {measurements_number[i]} in layer {i + 1} more than "
                  f"allowed {used_measurements_number} and {used_measurements_number} will be used.")
        if not is_allowable_first_plug_position(first_plug_position[i], 2 * dipole_distances[i]):
            used_first_plug_position = dipole_distances[i] * 2
            flash(
                f"First plug position {first_plug_position[i]} is too small and {used_first_plug_position} will be used.")
        layers.append(Layer(measurements_number=used_measurements_number,
                            step=step[i],
                            dipole_distance=dipole_distances[i],
                            first_plug_position=used_first_plug_position,
                            end_plug_position=end_plug_position[i],
                            first_point_for_measurement=first_points_for_measurements[i])
                      )

    return layers


def read_2d_file(path):
    """In this function will be loaded"""
    df = pd.read_csv(path, header=None)
    return df


def concatenate_layers_dataframes(layers):
    """In this function all layers will be changed to their dataframe representations and concatenated into 1 df"""
    res_df = layers[0].to_df()
    for i in range(1, len(layers)):
        res_df = res_df.append(layers[i].to_df())
        res_df.reset_index(inplace=True, drop=True)
    return res_df


def check_er_as_correct(df):
    """In this function will be checked currency of Resistivity values for recalculated dataframe"""
    return not ((df['ER_a'] > 10000).any() | (df['ER_a'] <= 0).any())


def filter_2d_df(df, layers):
    """In this function will be recalculated result dataframe"""
    res_df = concatenate_layers_dataframes(layers)  # concatenating all layers before recalculating

    try:
        res_df.loc[:, 'Resistivity'] = df[2].astype(float)
    except ValueError:
        res_df.loc[:, 'Resistivity'] = df[2].apply(lambda x: x.replace(',', '.'))
        res_df.loc[:, 'Resistivity'] = res_df['Resistivity'].astype(float)
    res_df.loc[:, 'a'] = res_df['B'] - res_df['A']
    res_df.loc[:, 'n'] = (res_df['M'] - res_df['B']) / res_df['a']
    res_df.loc[:, '1st_el'] = res_df['A']
    res_df.loc[:, 'K'] = math.pi * res_df['n'] * (res_df['n'] + 1) * (res_df['n'] + 2) * res_df['a']
    res_df.loc[:, 'ER_a'] = res_df['K'] * res_df['Resistivity']
    if check_er_as_correct(res_df):
        flash("There are values are out of bounds (0, 10.000);")
    return res_df


def save_to_dat(df: pd.DataFrame, path, title="CALC_FILE"):
    """In this function dataframe will be saved into *.dat file with :param path/*.dat"""
    # Header generation
    header = f"{title}\n"
    header += "1\n"
    header += f"{df.shape[0]}\n"
    header += "0\n0\n"
    header += "3\n"
    # body generation
    with open(path, 'w') as outfile:
        outfile.write(header)
        for row in df.iterrows():
            outfile.write("%.2f %.2f %.2f %.2f\n" % (row[1]['1st_el'], row[1]['a'], row[1]['n'], row[1]['ER_a']))
        # footer
        outfile.write("0\n0\n0\n0")
