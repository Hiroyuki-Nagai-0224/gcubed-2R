import pickle
from copy import deepcopy
from parameters_2R_179 import ModelParameters  # バージョン179用のパラメータクラスをインポート
from gcubed_model import run_model            # シミュレーション実行用の関数（仮想関数）

# ステップ1：ベースラインのモデル解と予測値を読み込む
with open("user_data/results/2R/179/baseline_solution.pickle", "rb") as f:
    baseline_solution = pickle.load(f)

# ステップ2：バージョン179のモデルパラメータを読み込む
params = ModelParameters()
print("元のTIM値:", params.TIM)

# ステップ3：最恵国待遇関税率（TIM）を25%増加させる
params.TIM *= 1.25
print("変更後のTIM値:", params.TIM)

# ステップ4：変更後のパラメータでシミュレーション実験を実行する
simulation_results = run_model(baseline_solution, params)

# ステップ5：シミュレーション結果を保存する
with open("user_data/results/2R/179/run_experiment_tariff25.pickle", "wb") as f:
    pickle.dump(simulation_results, f)

print("実験完了：TIMを25%増加させた結果が保存。")
