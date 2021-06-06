import csv
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class ConstantsFor1dCalculation:
    __default_k = {'K1': 1, 'K2': 10, 'K3': 100, 'K4': 1000, 'K5': 10000, 'K6': 100000, 'K7': 1000000, 'K8': 10000000,
                   'K9': 100000000}
    __AB_mode = {'14m': 1, '30m': 2, 'Custom': 3}
    __AB = {'14m': [28., 24., 20., 18., 16., 14., 12., 10., 9., 8., 7., 6., 5., 4., 3., 2.],
            '30m': [60., 50., 40., 36., 32., 28., 24., 20., 18., 16., 14., 12., 10., 8., 6.],
            'Custom': []}

    @classmethod
    def ab(cls):
        return cls.__AB

    @classmethod
    def default_k(cls):
        return cls.__default_k

    @classmethod
    def ab_mode(cls):
        return cls.__AB_mode


def generate_1_calculation(path, calculation_size):
    df = pd.read_csv(path, header=None)
    # df.reset_index(drop=True, inplace=True)
    # print(df)
    for i in range(int(len(df) / calculation_size)):
        yield df[i * calculation_size:(i + 1) * calculation_size]


def filter_1d_table(df, mode=1, AB_values=None, MN_values=None, k=1):
    df.reset_index(drop=True, inplace=True)
    res_df = pd.DataFrame()
    res_df.loc[:, 'ER-1'] = df[2].astype(float)
    res_df.loc[:, 'K-taken'] = pd.Series([k] * df[2].shape[0])
    res_df.loc[:, 'AB'] = pd.Series(AB_values)
    print(res_df)
    if mode == 1:
        res_df.loc[:, 'MN'] = res_df['AB'].apply(lambda x: 2 if x > 10 else 1)
    elif mode == 2:
        res_df.loc[:, 'MN'] = pd.Series([2] * df[2].shape[0])
    elif mode == 3:
        user_ab = np.array(list(map(lambda x: float(x.strip()), AB_values.split(','))))
        res_df.loc[:, 'AB'] = user_ab
        mn_column = pd.Series([])
        for i in range(len(res_df['AB'])):
            for key, value in MN_values.sort().items():
                if res_df['AB'][i] / 2. > float(key):
                    mn_column[i] = float(value)
    res_df.loc[:, 'AB-half'] = res_df['AB'] / 2.
    # todo: disable scientific mode for source table
    return res_df


def calculate_k_multiply(AB_half: float, MN: float = 2) -> float:
    return math.pi * (AB_half - MN / 2) * (AB_half + MN / 2) / MN


def recalcule_ER(AB_half: float, k_set, r):
    return r * calculate_k_multiply(AB_half) / k_set


def recalculate_table(df: pd.DataFrame):
    recalculating_columns = [col_name for col_name in df.columns if
                             df[col_name].isna().sum() == 0 and col_name.startswith('ER')]
    # print(recalculating_columns)
    for column in recalculating_columns:
        df.loc[:, column] = df.apply(lambda row: recalcule_ER(row['AB-half'], row['K-taken'], row[column]), axis=1)
        df.loc[:, column] = df[column].apply(lambda x: '{:.3f}'.format(x))

    return df


def calculate_pseudo_depth(df):
    df.loc[:, 'Pseudo-depth'] = df['AB-half'] / 1.5


def plot_1d(df, path_to_save):
    fig = plt.figure(figsize=[12, 8])

    ax = fig.add_subplot(111)
    ax.xaxis.tick_top()
    ax.set_xlabel('Electrical Resistivity, Ohm m', weight='bold', fontsize=13, labelpad=12)
    ax.xaxis.set_label_position('top')
    ax.set_ylabel('Pseudo-depth, m', weight='bold', fontsize=13)
    plt.ylim(df['Pseudo-depth'].max() + 5, df['Pseudo-depth'].min() - 5)
    ax.plot(df['ER-1'], df['Pseudo-depth'], label='ER-1', c='brown')
    # todo: make plot of ER-# without
    # ax.plot(df['ER-2'], df['Pseudo-depth'], label='ER-2')
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_to_save)
