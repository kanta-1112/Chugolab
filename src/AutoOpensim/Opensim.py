import opensim # type: ignore

# モデルと解析セットアップファイルのパス
model_path = "your_model.osim"
setup_path = "setup_analyze.xml"

# AnalyzeToolのインスタンス作成
analyze_tool = opensim.AnalyzeTool(setup_path)
analyze_tool.setModelFilename(model_path)
analyze_tool.run()