import math
from enum import Enum

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from flask import flash


class ConstantsFor1dCalculation(Enum):
    """Class with constants for 1D calculation"""
    default_k = {'K0': 1, 'K1': 10, 'K2': 100, 'K3': 1_000, 'K4': 10_000, 'K5': 10_0000, 'K6': 1_000_000,
                 'K7': 10_000_000, 'K8': 100_000_000, 'K9': 1_000_000_000, 'Custom': None}
    AB_mode = {'14m': 1, '30m': 2, '40m': 3, 'Custom': 4}
    AB = {'14m': [28., 24., 20., 18., 16., 14., 12., 10., 9., 8., 7., 6., 5., 4., 3., 2.],
          '30m': [2] * 15,
          '40m': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0,
                  2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
                  ],
          'Custom': []}
    MN = {'14m': [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          '30m': [60., 50., 40., 36., 32., 28., 24., 20., 18., 16., 14., 12., 10., 8., 6.],
          '40m': [120., 110., 100., 90., 80., 70., 60., 50., 50., 44., 40., 36., 32., 30., 30., 28., 26., 24., 22.,
                  20., 18., 16., 14., 12., 12., 10., 8., 6., 4., 2.],
          'Custom': []}


def concatenate_all_dataframes(list_of_dataframes):
    """This function will concatenate all dataframes by column"""
    # taking first dataframe as start dataframe and delete this df from list
    initial_dataframe = list_of_dataframes.pop(0)
    for i, df in enumerate(list_of_dataframes):
        initial_dataframe.insert(0, f'ER-{i + 2}', df['ER-1'], True)
        initial_dataframe.reset_index(drop=True, inplace=True)
    return initial_dataframe


def generate_1_calculation(path, calculation_size):
    if path is not None:
        df = pd.read_csv(path, header=None)
    else:
        return
    try:
        for i in range(int(len(df) / calculation_size)):
            yield df[i * calculation_size:(i + 1) * calculation_size]
    except ZeroDivisionError:
        flash('Incorrect size of AB array')


def filter_1d_table(df, mode=1, AB_values=None, MN_values=None, k=1):
    """In this function will be generated 1d table for 1d calculation"""
    df.reset_index(drop=True, inplace=True)
    res_df = pd.DataFrame()
    res_df.loc[:, 'ER-1'] = df[2].astype(float)
    res_df.loc[:, 'K-taken'] = pd.Series([k] * df[2].shape[0])
    res_df.loc[:, 'AB'] = pd.Series(AB_values)
    res_df.loc[:, 'MN'] = pd.Series(MN_values)
    res_df.loc[:, 'AB-half'] = res_df['AB'] / 2.
    # todo: disable scientific mode for source table
    return res_df


def calculate_k_multiply(ab_half: float, mn: float = 2) -> float:
    """In this function will be calculated K for next calculations of ER"""
    return math.pi * (ab_half - mn / 2) * (ab_half + mn / 2) / mn


def recalculate_er(ab_half: float, k_set, r):
    """In this function will be recalculated one ER param"""
    return r * calculate_k_multiply(ab_half) / k_set


def recalculate_table(df: pd.DataFrame):
    """In this function will be recalculated all ER parameters of dataframe"""
    # Claiming all columns that starts with ER in dataframe
    recalculating_columns = [col_name for col_name in df.columns if
                             df[col_name].isna().sum() == 0 and col_name.startswith('ER')]
    # Recalculating this functions
    for column in recalculating_columns:
        df.loc[:, column] = df.apply(lambda row: recalculate_er(row['AB-half'], row['K-taken'], row[column]), axis=1)
        df.loc[:, column] = df[column].apply(lambda x: '{:.3f}'.format(x))

    return df


def calculate_pseudo_depth(df):
    """In this function will be calculated pseudo_depth parameter for charts"""
    df.loc[:, 'Pseudo-depth'] = df['AB-half'] / 1.5


def plot_1d(df, path_to_save, index):
    """In this function will be generated and saved 1D plot"""
    fig = plt.figure(figsize=[12, 8])
    ax = fig.add_subplot(111)
    ax.xaxis.tick_top()
    ax.set_xlabel('Electrical Resistivity, Ohm m', weight='bold', fontsize=13, labelpad=12)
    ax.xaxis.set_label_position('top')
    ax.set_ylabel('Pseudo-depth, m', weight='bold', fontsize=13)
    plt.ylim(df['Pseudo-depth'].max() + 5, df['Pseudo-depth'].min() - 5)
    ax.plot(df['ER-1'].apply(lambda x: float(x)), df['Pseudo-depth'], label=f'ER-{index + 1}', c='blue')
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_to_save)
