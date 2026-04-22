import random
from typing import Dict, Any, List
from basic.error.base_error import BusinessError
from biz_module.model.quiz_question_model import QuizQuestionModel
from biz_module.model.quiz_outcome_model import QuizOutcomeModel
from biz_module.utils.quiz_algo.base import BaseQuizAlgo


class RandomAlgo(BaseQuizAlgo):
    """
    加权随机算法（适用于塔罗、运势等类型）
    按各 outcome 的 match_config.weight 加权随机选取
    """

    def calculate(
        self,
        answers: Dict[str, str],
        questions: List[QuizQuestionModel],
        outcomes: List[QuizOutcomeModel],
        algo_config: Dict[str, Any],
        special_rules: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        special_code = self.check_special_rules(answers=answers, special_rules=special_rules)
        if special_code:
            return {"outcome_code": special_code, "score": None, "calc_result": {"triggered_by": "special_rule"}}

        normal_outcomes = [o for o in outcomes if not o.is_special and not o.is_fallback]
        if not normal_outcomes:
            raise BusinessError("未配置可用结果")

        weights = [
            (o.match_config or {}).get("weight", 1) for o in normal_outcomes
        ]
        selected = random.choices(normal_outcomes, weights=weights, k=1)[0]

        return {
            "outcome_code": selected.code,
            "score": None,
            "calc_result": {},
        }
