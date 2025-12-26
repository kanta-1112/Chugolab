# -*- coding: shift_jis -*-
import pandas as pd
import numpy as np

# ファイルを読み込み、空の列を削除する
df = pd.read_csv(r"C:\\study\\Prac_Programming\\prac_Python\\Chugolab\\prog_data1.csv", header=None).dropna(axis=1, how='all')

# DataFrameをNumPy配列に変換
prog_data_array = df.to_numpy(dtype=float)

# 上の行と下の行をそれぞれ別の配列に分割する
first_row_array = prog_data_array[0, :]
second_row_array = prog_data_array[1, :]
fourth_row_array = prog_data_array[3, :]
fifth_row_array = prog_data_array[4, :]

# 分割された配列とそのサイズを表示
print("--- 1行の配列 ---")
print(first_row_array)
print("\n配列のサイズ:", first_row_array.shape)

print("\n--- 2行の配列 ---")
print(second_row_array)
print("\n配列のサイズ:", second_row_array.shape)

print("--- 4行の配列 ---")
print(fourth_row_array)
print("\n配列のサイズ:", fourth_row_array.shape)

print("\n--- 5行の配列 ---")
print(fifth_row_array)
print("\n配列のサイズ:", fifth_row_array.shape)
