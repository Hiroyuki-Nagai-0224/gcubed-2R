"""
Simulation experiment: 最恵国待遇関税率（TIM）を25％引き上げるシナリオ
"""

import os
import pickle
import logging
import gcubed
import gcubed.projections
from gcubed.model import Model
from gcubed.projections.baseline_projections import BaselineProjections
from gcubed.projections.projections import Projections
from gcubed.linearisation.solved_model import SolvedModel
from gcubed.runners.simulation_runner import SimulationRunner
from model_constants import (
    CONFIGURATION,
    EXPERIMENT_RESULTS_FOLDER,
    EXPERIMENT_TARIFF_25 as EXPERIMENT,  # TIMを25％引き上げる実験設計ファイル
)

# 結果が保存されるフォルダを決定
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

# 既に生成済みのベースライン予測があれば読み込む
baseline_projections_pickle_file: str = os.path.join(
    results_folder, "baseline_projections.pickle"
)
if os.path.exists(baseline_projections_pickle_file):
    logging.info(
        f"既存のベースライン予測を {baseline_projections_pickle_file} から読み込みます。"
    )
    with open(baseline_projections_pickle_file, "rb") as file:
        baseline_projections: BaselineProjections = pickle.load(file)

# ベースライン予測が存在しない場合、モデルを解いてベースラインを再生成
if not (
    "baseline_projections" in globals()
    and isinstance(baseline_projections, BaselineProjections)
):
    # まずは解かれたモデル（solved_model）を読み込む
    solved_model_pickle_file: str = os.path.join(results_folder, "solved_model.pickle")
    if os.path.exists(solved_model_pickle_file):
        logging.info(f"以前に解かれたモデルを {solved_model_pickle_file} から読み込みます。")
        with open(solved_model_pickle_file, "rb") as file:
            solved_model: SolvedModel = pickle.load(file)

    if not ("solved_model" in globals() and isinstance(solved_model, SolvedModel)):
        model: Model = Model(configuration=CONFIGURATION)
        solved_model: SolvedModel = SolvedModel(model=model)
        with open(solved_model_pickle_file, "wb") as file:
            pickle.dump(solved_model, file)
        logging.info("解かれたモデルを保存しました。")

    baseline_projections: BaselineProjections = BaselineProjections(
        solved_model=solved_model
    )
    with open(baseline_projections_pickle_file, "wb") as file:
        pickle.dump(baseline_projections, file)
    logging.info("ベースライン予測を保存しました。")

# TIMを25%引き上げる実験シナリオ用の実験設計ファイル（EXPERIMENT_TARIFF_25）を用いてシミュレーションランナーを設定
runner: SimulationRunner = SimulationRunner(
    baseline_projections=baseline_projections,
    experiment_design_file=EXPERIMENT,
)

# シミュレーション実験の実行
runner.run()

# ■ ベースライン予測の保存 ■
baseline_projections: Projections = runner.baseline_projections
baseline_csv_path = os.path.join(
    results_folder,
    f"{baseline_projections.name}.csv",
)
baseline_projections.charting_projections.to_csv(baseline_csv_path)
logging.info(f"ベースライン予測を {baseline_csv_path} に保存しました。")

# ■ 最終予測の保存 ■
final_projections: Projections = runner.final_projections
final_csv_path = os.path.join(
    results_folder,
    f"{final_projections.name}.csv",
)
final_projections.charting_projections.to_csv(final_csv_path)
logging.info(f"最終予測を {final_csv_path} に保存しました。")

# ■ 乖離（deviations）の計算と保存 ■
deviations = gcubed.projections.deviations(
    new_projections=final_projections,
    original_projections=baseline_projections,
)
deviations_csv_path = os.path.join(
    results_folder,
    f"deviations of {final_projections.name} from {baseline_projections.name}.csv",
)
deviations.to_csv(deviations_csv_path)
logging.info(f"乖離結果を {deviations_csv_path} に保存しました。")
