
import opensim # type: ignore
import glob
import os

# モデルファイルのパス
model_path = "your_model.osim"
# motionファイルが入っているフォルダ
motion_folder = "motions/"
# AnalyzeセットアップXMLのテンプレート
setup_template = "setup_analyze.xml"
# 結果保存先の親フォルダ
results_root = "results/"

# motionファイル一覧を取得
motion_files = glob.glob(os.path.join(motion_folder, "*.mot"))

for motion_file in motion_files:
    analyze_tool = opensim.AnalyzeTool(setup_template)
    analyze_tool.setModelFilename(model_path)
    analyze_tool.setCoordinatesFileName(motion_file)
    # 出力フォルダ名をmotionファイルごとに分ける
    output_dir = os.path.join(results_root, os.path.splitext(os.path.basename(motion_file))[0])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    analyze_tool.setResultsDir(output_dir)
    analyze_tool.run()

     # 解析結果ファイル（例: output.txt）をExcel形式で保存
    txt_path = os.path.join(output_dir, "output.txt")
    xlsx_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(motion_file))[0]}.xlsx")
    if os.path.exists(txt_path):
        df = pd.read_csv(txt_path, sep='\t')  # 区切り文字は必要に応じて変更
        df.to_excel(xlsx_path, index=False)