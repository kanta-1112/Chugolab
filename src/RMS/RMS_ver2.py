import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------
#実装内容： ループ処理にして、一括ですべて見れるように
#次に入れたい内容：順位付けを行って、一番外れているものを見れるように。もしくは、2乗誤差以外の計算方法の実装
# ---------------------------------------------------------

# --- 設定パラメータ ---
START_INDEX = 1  # 処理を開始するデータ番号
END_INDEX = 30   # 処理を終了するデータ番号
BASE_DIR = r"C:\KAN\Program\2DKDE\2DKDE_data"
FILENAME_SUFFIX = ".csv"
BASE_FILENAME = "prog_data"

# 1. 正解データの読み込み
Correct_data_path = r"C:\KAN\Program\2DKDE\2DKDE_data\prog_data33.csv"

Correct_df = pd.read_csv(Correct_data_path, header=None).dropna(axis=1, how='all')
prog_data_array = Correct_df.to_numpy(dtype=float)

Correct_x_data = prog_data_array[0, :]
Correct_y_data = prog_data_array[1, :]

Correct_x = np.array(Correct_x_data)
Correct_y = np.array(Correct_y_data)

# ---------------------------------------------------------
# 2. 検証データの読み込み
for i in range(START_INDEX, END_INDEX + 1):
    filename = f"{BASE_FILENAME}{i}{FILENAME_SUFFIX}"
    Exp_data_path = os.path.join(BASE_DIR, filename)
    base_name = os.path.splitext(os.path.basename(Exp_data_path))[0] 

    Exp_df = pd.read_csv(Exp_data_path, header=None).dropna(axis=1, how='all')
    prog_data_array = Exp_df.to_numpy(dtype=float)

    Exp_x_data = prog_data_array[0, :]
    Exp_y_data = prog_data_array[1, :]

    Exp_x = np.array(Exp_x_data)
    Exp_y = np.array(Exp_y_data)

    # ---------------------------------------------------------
    # 3. 最小二乗誤差の計算
    # ---------------------------------------------------------

    # 念のためデータ長を揃える（短い方に合わせる）
    n = min(len(Correct_x), len(Exp_x))
    Correct_x_subset = Correct_x[:n]
    Exp_x_subset = Exp_x[:1]
    Correct_y_subset = Correct_y[:n]
    Exp_y_subset = Exp_y[:n]

    # X座標の差の二乗
    diff_x_sq = (Correct_x_subset - Exp_x_subset) ** 2

    # Y座標の差の二乗
    diff_y_sq = (Correct_y_subset - Exp_y_subset) ** 2

    # 合計（Sum of Squared Errors）
    sse = (diff_x_sq + diff_y_sq).sum()

    print(f"--- 検証データ: {i} ---")
    #print(f"データ点数: {n}")
    print(f"最小二乗誤差 (SSE): {sse}\n")