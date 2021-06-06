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
    for i in range(int(len(df) / calculation_size)):
        yield df[i * calculation_size:(i + 1) * calculation_size]


def concatenate_batch_of_calculations(list_of_dataframes):
    # taking first dataframe as start dataframe and delete this df from list
    initial_dataframe = list_of_dataframes.pop(0)
    for i, df in enumerate(list_of_dataframes):
        initial_dataframe.insert(0, f'ER-{i + 2}', df['ER-1'], True)
        initial_dataframe.reset_index(drop=True, inplace=True)
    return initial_dataframe


def filter_1d_table(df, mode=1, AB_values=None, MN_values=None, k=1):
    df.reset_index(drop=True, inplace=True)
    res_df = pd.DataFrame()
    res_df.loc[:, 'ER-1'] = df[2].astype(float)
    res_df.loc[:, 'K-taken'] = pd.Series([k] * df[2].shape[0])
    res_df.loc[:, 'AB'] = pd.Series(AB_values)
    # print(res_df)
    if mode == 1:
        res_df.loc[:, 'MN'] = res_df['AB'].apply(lambda x: 2 if x > 10 else 1)
    elif mode == 2:
        res_df.loc[:, 'MN'] = pd.Series([2] * df[2].shape[0])
    elif mode == 3:
        res_df.loc[:, 'MN'] = pd.Series([2] * res_df['AB'].shape[0])
        # mn_column = pd.Series([])
        # for i in range(len(res_df['AB'])):
        #     for key, value in MN_values.sort().items():
        #         if res_df['AB'][i] / 2. > float(key):
        #             mn_column[i] = float(value)
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


def plot_1d(df, path_to_save, plots_number=3):
    fig, axs = plt.subplots(1, plots_number, figsize=(16, 8), sharey=True)
    plot_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    plt.ylim(df['Pseudo-depth'].max() + 5, df['Pseudo-depth'].min() - 5)

    for i in range(plots_number):
        axs[i].xaxis.tick_top()
        axs[i].set_xlabel('Electrical Resistivity, Ohm m', weight='bold', fontsize=13, labelpad=12)
        axs[i].xaxis.set_label_position('top')
        axs[i].set_ylabel('Pseudo-depth, m', weight='bold', fontsize=13)

    for i in range(plots_number):
        axs[i].plot(df[f'ER-{i + 1}'].apply(lambda x: round(float(x), 2)), df['Pseudo-depth'], label=f'ER-{i + 1}',
                    c=plot_colors[i])
        axs[i].tick_params(axis='x', labelsize=14)
    # todo: make plot of ER-# without
    # ax.plot(df['ER-2'], df['Pseudo-depth'], label='ER-2')
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

    # finally we invoke the legend (that you probably would like to customize...)

    fig.legend(lines, labels, loc='lower right')
    plt.tight_layout()
    plt.savefig(path_to_save)
