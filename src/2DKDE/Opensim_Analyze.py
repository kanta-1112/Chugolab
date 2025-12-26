import opensim as osim
import os

# --- パスの設定 ---
# このパス設定は、実際の環境に合わせて変更してください。
# `H:\マイドライブ`はGoogle Driveの同期フォルダの可能性がありますが、
# モデルファイルは拡張子が`.osim`である必要があります。
#
# model_path = "H:\マイドライブ\Kwansei\4_spring\ChugoLab\MyResearch\model.osim"
# motion_path = "H:\マイドライブ\Kwansei\4_spring\ChugoLab\MyResearch\motion.mot"

# パスはWindowsの慣習に合わせて、バックスラッシュをエスケープするか、
# raw文字列（r"..."）を使用するのが安全です。
model_path = r"C:\ChugoLab\NEW1.osim"
motion_path = r"C:\ChugoLab\normal.mot"
states_file_path = r"C:\ChugoLab\subject01_Setup_IK.xml"
states_storage = osim.Storage(states_file_path)
results_dir = "Results"

def analyze_opensim(model_path, motion_path, states_storage, results_dir):
    """
    OpenSimのAnalyzeを実行する関数
    :param model_path: OpenSimモデルファイルのパス
    :param motion_path: モーションデータファイルのパス
    :param results_dir: 結果を保存するディレクトリ
    """
    # 既存の結果ディレクトリを削除し、新しく作成
    # 複数回実行する際に前の結果が残らないようにするため
    if os.path.exists(results_dir):
        os.system(f"rd /s /q {results_dir}")  # Windowsの場合
        # os.system(f"rm -r {results_dir}")  # Linux/macOSの場合
    os.makedirs(results_dir)

    print(f"モデルをロード中: {model_path}")
    try:
        model = osim.Model(model_path)
        print("モデルのロードが完了しました。")
    except Exception as e:
        print(f"モデルのロード中にエラーが発生しました: {e}")
        return

    # AnalyzeToolのセットアップ
    analyze_tool = osim.AnalyzeTool()
    analyze_tool.setModel(model)
    analyze_tool.setCoordinatesFileName(motion_path)
    analyze_tool.setStatesStorage(states_storage)
    analyze_tool.setResultsDir(results_dir)
    analyze_tool.setInitialTime(0)
    analyze_tool.setFinalTime(-1)  # -1は全フレーム

    # 解析設定の追加
    # BodyKinematics解析
    body_kin = osim.BodyKinematics()
    body_kin.setStepInterval(1)  # 1ステップごとに解析結果を生成
    analyze_tool.getAnalysisSet().adoptAndAppend(body_kin)

    # Kinematics解析
    kin = osim.Kinematics()
    kin.setStepInterval(1)
    analyze_tool.getAnalysisSet().adoptAndAppend(kin)

    # 解析の実行
    print("解析を開始します...")
    try:
        analyze_tool.run()
        print("解析が完了しました。")
        print(f"結果は {results_dir} に保存されました。")
    except Exception as e:
        print(f"解析中にエラーが発生しました: {e}")

# スクリプトの実行
analyze_opensim(model_path, motion_path, states_storage, results_dir)