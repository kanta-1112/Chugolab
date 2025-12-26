import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.stats import gaussian_kde
import os # ファイル操作のためにosモジュールを追加

# ---------------------------------------------------------
#実装内容：矢状平面図の透過表示

# 初期重心の位置をプロット
# 第1相から第2相と第2相から第3相でそれぞれ2DKDEを行う
# 単データに限定して、二次元カーネル密度推定を行うコード
# ---------------------------------------------------------

# 1. お手持ちのデータを読み込む (この部分をあなたのデータに合わせて変更してください)
data_path = r"C:\\study\\Prac_Programming\\prac_Python\\Chugolab\\2DKDE_data\\prog_data33.csv"

# 画像ファイルのパスを指定
img_path = r"C:\\study\\Prac_Programming\\prac_Python\\Chugolab\\3model.png"
# 画像を読み込み
img = mpimg.imread(img_path)

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
plt.figure(figsize=(5, 8), facecolor="white")

# 画像を表示する
plt.imshow(img, extent=[xmin, xmax/2, ymin/2, ymax], alpha=0.8)

# 散布図で元のデータをプロット（背景として）
plt.scatter(x1, y1, s=10, alpha=0.3, label='1⇒2')
plt.scatter(x2, y2, s=10, alpha=0.3, label='2⇒3')
plt.scatter(x0, y0, s=50, alpha=1.0, label='FirstPosition')

# 等高線図で密度をプロット
plt.contourf(xi, yi, density1, levels=10, cmap='Reds', alpha=0.5)
plt.contourf(xi, yi, density2, levels=10, cmap='Blues', alpha=0.4)
plt.colorbar(label='Density') # 密度を示すカラーバー

plt.tick_params(axis='both', which='major', labelsize=14) # 'labelsize'を希望のサイズに変更
plt.title('2D Kernel Density Estimation', fontsize=16)
plt.xlabel('X-axis', fontsize=14)
plt.ylabel('Y-axis', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
output_filename = f"{base_name}.png"
plt.savefig(output_filename) # 画像として保存
plt.show()

print(f"お手持ちのデータで二次元カーネル密度推定が完了し、'{output_filename}'として保存されました。")