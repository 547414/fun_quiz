from typing import Dict, Any, List
from basic.error.base_error import BusinessError
from biz_module.model.quiz_question_model import QuizQuestionModel
from biz_module.model.quiz_outcome_model import QuizOutcomeModel
from biz_module.utils.quiz_algo.base import BaseQuizAlgo


class ScoreAlgo(BaseQuizAlgo):
    """
    累分段映射算法（适用于「恋爱脑指数」等类型）
    汇总所有选项分值，按区间匹配 outcome
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
            special_outcome = next((o for o in outcomes if o.code == special_code), None)
            if special_outcome:
                return {"outcome_code": special_code, "score": None, "calc_result": {"triggered_by": "special_rule"}}

        total_score = 0
        for question in questions:
            if question.is_hidden:
                continue
            answer_key = answers.get(str(question.seq))
            if not answer_key:
                continue
            option = next((o for o in question.options if o.key == answer_key), None)
            if option:
                total_score += option.score or 0

        total_max = algo_config.get("total_max", 100)
        score_pct = int(total_score / total_max * 100) if total_max > 0 else 0

        normal_outcomes = [o for o in outcomes if not o.is_special and not o.is_fallback]
        fallback_outcome = next((o for o in outcomes if o.is_fallback), None)

        matched = None
        for outcome in normal_outcomes:
            cfg = outcome.match_config or {}
            score_min = cfg.get("score_min", 0)
            score_max = cfg.get("score_max", 0)
            if score_min <= total_score <= score_max:
                matched = outcome
                break

        if not matched:
            if fallback_outcome:
                return {"outcome_code": fallback_outcome.code, "score": score_pct, "calc_result": {"total_score": total_score}}
            raise BusinessError("未找到匹配的结果区间")

        return {
            "outcome_code": matched.code,
            "score": score_pct,
            "calc_result": {"total_score": total_score},
        }
