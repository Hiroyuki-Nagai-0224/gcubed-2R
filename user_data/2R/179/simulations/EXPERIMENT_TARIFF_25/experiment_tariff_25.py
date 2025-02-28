"""
TIMを25％引き上げるシナリオ（2025年にエージェントがこの変化を認識）
"""

EXPERIMENT_TARIFF_25 = {
    "start_year": 2025,  # ショックが発生する年
    "shocks": {
        "TIM": {  # 最恵国待遇関税率
            "USA": 1.25,  # TIMを25%増加
        }
    }
}
