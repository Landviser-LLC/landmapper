import csv
import math
import pandas as pd
import matplotlib.pyplot as plt


# from pygimli.physics import ert


# def show_2d(path, path_to_save):
#     fig, ax = plt.subplots(1, 1)
#     schemeName = 'dd'
#     s = ert.load(path, elecs=4)
#     k = ert.geometricFactors(s)
#     _ = ert.show(s, vals=k, label='k - ' + schemeName)

#    plt.savefig(path_to_save)


def transform_1d_input(path1, k, AB):
    with open(path1, "r", newline="") as file1:
        reader = csv.reader(file1)
        datalist = []
        for row in reader:
            datalist.append([row[0], row[2], row[3], row[4], row[5], row[7], row[9], AB, k, ])
        resdf = pd.DataFrame(datalist, columns=['№', 'ER-1', 'K#', 'day of the month', 'timestamp', 'voltage',
                                                'amperage'])
    return resdf


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
    return df


def calculate_pseudo_depth(df):
    df.loc[:, 'Pseudo-depth'] = df['AB-half'] / 1.5


def plot_1d(df, path_to_save):
    fig = plt.figure(figsize=[8, 8])

    ax = fig.add_subplot(111)
    ax.xaxis.tick_top()
    ax.set_xlabel('Electrical Resistivity, Ohm m', weight='bold', fontsize=13, labelpad=12)
    ax.xaxis.set_label_position('top')
    ax.set_ylabel('Pseudo-depth, m', weight='bold', fontsize=13)
    plt.ylim(df['Pseudo-depth'].max() + 5, df['Pseudo-depth'].min() - 5)
    ax.plot(df['ER-1'], df['Pseudo-depth'], label='ER-1', c='brown')
    ax.plot(df['ER-2'], df['Pseudo-depth'], label='ER-2')
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_to_save)
