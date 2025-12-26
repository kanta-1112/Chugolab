import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

# ---------------------------------------------------------
#実装内容：初期重心の位置をプロット

# 第1相から第2相と第2相から第3相でそれぞれ2DKDEを行う
# 単データに限定して、二次元カーネル密度推定を行うコード
# ---------------------------------------------------------

# 1. お手持ちのデータを読み込む (この部分をあなたのデータに合わせて変更してください)
data_path = r"C:\\study\\Prac_Programming\\prac_Python\\Chugolab\\2DKDE_data\\prog_data31_ver2.csv"

# ファイルパスから拡張子なしのファイル名を抽出
base_name = os.path.splitext(os.path.basename(data_path))[0] 

df = pd.read_csv(data_path, header=None).dropna(axis=1, how='all')
prog_data_array = df.to_numpy(dtype=float)

my_x_data1 = prog_data_array[0, :]
my_y_data1 = prog_data_array[1, :]
my_x_data2 = prog_data_array[2, :]
my_y_data2 = prog_data_array[3, :]
my_x_data0 = prog_data_array[4, :]
my_y_data0 = prog_data_array[5, :]

x1 = np.array(my_x_data1)
y1 = np.array(my_y_data1)
x2 = np.array(my_x_data2)
y2 = np.array(my_y_data2)
x0 = my_x_data0
y0 = my_y_data0



# 2. 二次元カーネル密度推定の実行
xy1 = np.vstack([x1, y1])
kde1 = gaussian_kde(xy1,bw_method=0.5)
xy2 = np.vstack([x2, y2])
kde2 = gaussian_kde(xy2,bw_method=0.5)
# bw_methodはカーネルの帯域幅を調整するパラメータです。


# 3. KDEを評価するためのグリッドの作成
xmin, ymin = -0.6, 0
xmax, ymax = 0.3, 1.2


# グリッドポイントの作成
xi, yi = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
# 評価用の座標をスタック
coords = np.vstack([xi.ravel(), yi.ravel()])

# グリッド上の各点でKDEの確率密度を評価
density1 = kde1(coords).reshape(xi.shape)
density2 = kde2(coords).reshape(xi.shape)
# 4. 結果のプロット
plt.figure(figsize=(10, 8))

# 散布図で元のデータをプロット（背景として）
plt.scatter(x1, y1, s=10, alpha=0.5, label='1⇒2')
plt.scatter(x2, y2, s=10, alpha=0.5, label='2⇒3')
plt.scatter(x0, y0, s=50, alpha=0.9, color='green', label='FirstPosition', zorder=10)

# 等高線図で密度をプロット
plt.contourf(xi, yi, density1, levels=10, cmap='Reds', alpha=0.8)
plt.contourf(xi, yi, density2, levels=10, cmap='Blues', alpha=0.3)

cbar = plt.colorbar(label='Density') 
# 2. カラーバーの目盛り数字のサイズを変更 (例: 14)
cbar.ax.tick_params(labelsize=24) 
# 3. カラーバーのラベル（タイトル）のサイズを変更 (例: 16)
cbar.set_label('Density', fontsize=24) 

plt.tick_params(axis='both', which='major', labelsize=20) # 'labelsize'を希望のサイズに変更
#plt.title('2D Kernel Density Estimation', fontsize=16)
plt.xlabel('X-axis', fontsize=30)
plt.ylabel('Y-axis', fontsize=30)
plt.legend(fontsize=16)
plt.grid(True, linestyle='--', alpha=0.6)
output_filename = f"{base_name}.png"
plt.savefig(output_filename) # 画像として保存
plt.show()
print("お手持ちのデータで二次元カーネル密度推定が完了し、'data.png'として保存されました。")