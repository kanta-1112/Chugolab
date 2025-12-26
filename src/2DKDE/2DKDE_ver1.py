import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ---------------------------------------------------------
#実装内容： 単データに限定して、二次元カーネル密度推定を行うコード
# ---------------------------------------------------------

# 1. お手持ちのデータを読み込む 
data_path = r"C:\\study\\Prac_Programming\\prac_Python\\Chugolab\\new_prog_data1.csv"

# ここでは仮のデータを置きます。実際にはあなたのデータに置き換えてください。
df = pd.read_csv(data_path, header=None).dropna(axis=1, how='all')
prog_data_array = df.to_numpy(dtype=float)

my_x_data = prog_data_array[0, :]
my_y_data = prog_data_array[1, :]

x = np.array(my_x_data)
y = np.array(my_y_data)

# 2. 二次元カーネル密度推定の実行
xy = np.vstack([x, y])
kde = gaussian_kde(xy,bw_method=0.5)
# bw_methodはカーネルの帯域幅を調整するパラメータです。


# 3. KDEを評価するためのグリッドの作成
xmin, ymin = -0.6, 0
xmax, ymax = 0.3, 1.2


# グリッドポイントの作成
xi, yi = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
# 評価用の座標をスタック
coords = np.vstack([xi.ravel(), yi.ravel()])

# グリッド上の各点でKDEの確率密度を評価
density = kde(coords).reshape(xi.shape)

# 4. 結果のプロット
plt.figure(figsize=(10, 8))

# 散布図で元のデータをプロット（背景として）
plt.scatter(x, y, s=10, alpha=0.5, label='Original Data')

# 等高線図で密度をプロット
plt.contourf(xi, yi, density, levels=10, cmap='viridis', alpha=0.8)
plt.colorbar(label='Density') # 密度を示すカラーバー

plt.title('2D Kernel Density Estimation with Your Data')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('2d_kde_plot_your_data.png') # 画像として保存
plt.show()

print("お手持ちのデータで二次元カーネル密度推定が完了し、'2d_kde_plot_your_data.png'として保存されました。")