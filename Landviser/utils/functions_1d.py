import csv
import math
import pandas as pd


def calculate_k_multiply(AB_half: float, MN: float = 2) -> float:
    return math.pi * (AB_half - MN / 2) * (AB_half + MN / 2) / MN


def recalcule_ER(AB_half: float, k_set, r):
    return r * calculate_k_multiply(AB_half) / k_set


def recalculate_table(df):
    recalculating_columns = ['ER-1', 'ER-2']
    for column in recalculating_columns:
        df.loc[:, column] = df.apply(lambda row: recalcule_ER(row['AB-half'], row['K-taken'], row[column]), axis=1)
    return df
