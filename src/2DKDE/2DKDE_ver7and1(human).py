import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os
import matplotlib.image as mping

# ---------------------------------------------------------
#実装内容：データの正規化．prog_dataに補正係数の2行を追加

# 異なる足首角度の初期条件a(0°,10°,20°)ごとに画像データを生成
# ループ処理にして、一括で33人分の画像データを生成
# 矢状平面図の透過表示
# バンド幅の調整
# 初期重心の位置をプロット
# 第1相から第2相と第2相から第3相でそれぞれ2DKDEを行う
# 単データに限定して、二次元カーネル密度推定を行うコード
# ---------------------------------------------------------

# --- 設定パラメータ ---
START_INDEX = 1  # 処理を開始するデータ番号
END_INDEX = 33   # 処理を終了するデータ番号

#各データの重心の初期位置ごとにいくつのデータがあるか
MASS_DATA_NUM = [72,72,24]

MASS_DATA_FIRST = [3,3,1]
MASS_DATA_ANGLE = [0,10,20]

# データファイルのディレクトリとベースファイル名を指定
BASE_DIR = r"C:\KAN\KAN's_research\data\input\prog_data\Normalize\2024"
OUT_DIR = r"C:\KAN\KAN's_research\data\output\PNG\20260203"
BASE_FILENAME = "prog_data"
FILENAME_SUFFIX = ".csv"

img_path = r"C:\KAN\KAN's_research\data\input\prog_data\Normalize\2024\model.png"
img = mping.imread(img_path)
# --------------------

# ループ処理: START_INDEX から END_INDEX までのすべてのデータファイルを処理
for i in range(START_INDEX, END_INDEX + 1):
    # ファイルパスを動的に生成
    filename = f"{BASE_FILENAME}{i}{FILENAME_SUFFIX}"
    data_path = os.path.join(BASE_DIR, filename)

    print(f"--- 処理を開始: {data_path} ---")

    # ファイルの存在チェック
    if not os.path.exists(data_path):
        print(f"エラー: ファイルが見つかりません: {data_path}")
        continue # 次の番号に進む

    try:
        start_col = 0

        for j in range(len(MASS_DATA_NUM)):

            data_count = MASS_DATA_NUM[j]
            end_col = start_col + data_count

            # 1. データを読み込む
            base_name = os.path.splitext(os.path.basename(data_path))[0] 
            
            df = pd.read_csv(data_path, header=None).dropna(axis=1, how='all')
            prog_data_array = df.to_numpy(dtype=float)

            # データの割り当て（元のコードと同じ）
            my_x_data1 = prog_data_array[0, start_col:end_col]
            my_y_data1 = prog_data_array[1, start_col:end_col]
            my_x_data2 = prog_data_array[2, start_col:end_col]
            my_y_data2 = prog_data_array[3, start_col:end_col]
            my_x_data0 = prog_data_array[4, MASS_DATA_FIRST[j]]
            my_y_data0 = prog_data_array[5, MASS_DATA_FIRST[j]]
            coefficient_X = prog_data_array[6,MASS_DATA_FIRST[j]]
            coefficient_Y = prog_data_array[7,MASS_DATA_FIRST[j]]

            x1 = np.array(my_x_data1)*coefficient_X
            y1 = np.array(my_y_data1)*coefficient_Y
            x2 = np.array(my_x_data2)*coefficient_X
            y2 = np.array(my_y_data2)*coefficient_Y
            x0 = my_x_data0*coefficient_X
            y0 = my_y_data0*coefficient_Y

            # 2. 二次元カーネル密度推定の実行
            xy1 = np.vstack([x1, y1])
            kde1 = gaussian_kde(xy1, bw_method=0.5)
            xy2 = np.vstack([x2, y2])
            kde2 = gaussian_kde(xy2, bw_method=0.5)

            # 3. KDEを評価するためのグリッドの作成
            xmin, ymin = -0.6, 0
            xmax, ymax = 0.3, 1.2

            xi, yi = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
            coords = np.vstack([xi.ravel(), yi.ravel()])

            # グリッド上の各点でKDEの確率密度を評価
            density1 = kde1(coords).reshape(xi.shape)
            density2 = kde2(coords).reshape(xi.shape)

            # 4. 結果のプロット
            plt.figure(figsize=(10, 8))

            plt.imshow(img, extent=[xmin+0.09, 0.09+xmax/2, -0.01+ymin/2, -0.01+ymax], alpha=1)

            # 散布図で元のデータをプロット（背景として）
            plt.scatter(x1, y1, s=10, alpha=0.5, label='1⇒2')
            plt.scatter(x2, y2, s=10, alpha=0.5, label='2⇒3')
            plt.scatter(x0, y0, s=50, alpha=0.9, color='green', label='FirstPosition', zorder=10)

            # 等高線図で密度をプロット
            plt.contourf(xi, yi, density1, levels=10, cmap='Reds', alpha=0.8)
            plt.contourf(xi, yi, density2, levels=10, cmap='Blues', alpha=0.3)

            cbar = plt.colorbar(label='Density') 
            # カラーバーの目盛りとラベルのサイズ設定
            cbar.ax.tick_params(labelsize=24) 
            cbar.set_label('Density', fontsize=24) 

            plt.tick_params(axis='both', which='major', labelsize=20)
            # タイトルにデータ番号を追加
            plt.title(f'2D KDE for {base_name}', fontsize=20) 
            plt.xlabel('X-axis', fontsize=30)
            plt.ylabel('Y-axis', fontsize=30)
            plt.legend(fontsize=16)
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # 出力ファイル名: 例 prog_data7.png
            output_filename = f"{MASS_DATA_ANGLE[j]}_{base_name}.png"
            
            # 出力ディレクトリ（データファイルと同じ場所）に保存
            output_path = os.path.join(OUT_DIR, output_filename)
            plt.savefig(output_path,transparent = False)
            
            plt.close() # メモリ節約のため、プロットウィンドウを閉じる
            
            print(f"✅ 処理完了: '{output_path}'として保存されました。")

    except Exception as e:
        print(f"⚠️ エラーが発生しました ({filename}): {e}")
        plt.close() # エラー時も念のため閉じる

print("\n--- 全てのデータの処理が終了しました ---")