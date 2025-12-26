import pandas as pd
import numpy as np
from pathlib import Path

def collect_center_of_mass_horizontal_no_repeat_time():
    # ================= 設定エリア =================
    base_folder_path = r"C:\KAN\KAN's_research\data\input\Simulation_result(2025)\2(1218)" 
    
    # 対象ファイル名
    target_file_name = "STSmodel_BodyKinematics_pos_global.sto"
    
    # 保存するファイル名
    output_filename = "2(1226).xlsx"
    # ==============================================

    root_path = Path(base_folder_path)
    dfs_to_concat = [] 

    print(f"'{target_file_name}' の探索を開始します...")
    
    # フォルダ名順にソート（重要：これでどのデータが最初に来るか決まります）
    target_files = list(root_path.rglob(target_file_name))
    target_files.sort(key=lambda x: x.parent.name)

    if not target_files:
        print(f"ファイル '{target_file_name}' が見つかりませんでした。")
        return

    # ループ回数（i）を使って、最初（i=0）かそれ以外かを判断します
    for i, file_path in enumerate(target_files):
        try:
            # 1. ヘッダー終了位置検出
            header_end_line = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_idx, line in enumerate(f):
                    if 'endheader' in line:
                        header_end_line = line_idx + 1
                        break
            
            # 2. データ読み込み
            df = pd.read_csv(file_path, sep='\t', skiprows=header_end_line, header=0)
            
            # 列があるか確認
            if not all(col in df.columns for col in ['time', 'center_of_mass_X', 'center_of_mass_Y']):
                print(f"× スキップ（列不足）: {file_path.parent.name}")
                continue

            cond_name = file_path.parent.name

            # 3. 列の抽出（ここが変更点）
            if i == 0:
                # --- 1つ目のファイル：Timeを含める ---
                subset = df[['time', 'center_of_mass_X', 'center_of_mass_Y']].copy()
                # 列名をつける（Timeは共通なので単に "time" としました）
                subset.columns = ['time', f'X_{cond_name}', f'Y_{cond_name}']
            else:
                # --- 2つ目以降のファイル：Timeを入れない ---
                subset = df[['center_of_mass_X', 'center_of_mass_Y']].copy()
                subset.columns = [f'X_{cond_name}', f'Y_{cond_name}']
            
            # 4. 右隣に空白列（仕切り）を追加
            subset[' '] = np.nan 

            dfs_to_concat.append(subset)
            print(f"○ 読込: {cond_name} {'(Timeあり)' if i==0 else '(Timeなし)'}")

        except Exception as e:
            print(f"エラー: {file_path.parent.name} - {e}")

    # 結合して保存
    if dfs_to_concat:
        print("データを結合しています...")
        final_df = pd.concat(dfs_to_concat, axis=1)
        
        # 最後の余分な空白列を削除
        if final_df.columns[-1] == ' ':
            final_df = final_df.iloc[:, :-1]

        save_path = root_path / output_filename
        
        try:
            final_df.to_excel(save_path, index=False)
            print("-" * 30)
            print(f"完了！ '{save_path}' に保存しました。")
        except ValueError:
            csv_path = root_path / "重心データ_横並びまとめ_Time整理版.csv"
            final_df.to_csv(csv_path, index=False)
            print("注意: 行数が多いためCSV形式で保存しました。")
    else:
        print("データが見つかりませんでした。")

if __name__ == "__main__":
    collect_center_of_mass_horizontal_no_repeat_time()