from typing import Dict, Any, List
from basic.error.base_error import BusinessError
from biz_module.model.quiz_question_model import QuizQuestionModel
from biz_module.model.quiz_outcome_model import QuizOutcomeModel
from biz_module.utils.quiz_algo.base import BaseQuizAlgo


class VectorAlgo(BaseQuizAlgo):
    """
    多维向量匹配算法（适用于 SBTI/MBTI 等类型）
    Step1: 按维度汇总原始分
    Step2: 原始分归档为 L=1 / M=2 / H=3
    Step3: 与各 outcome 的 dim_vector 计算曼哈顿距离，取最近者
    """

    def calculate(
        self,
        answers: Dict[str, str],
        questions: List[QuizQuestionModel],
        outcomes: List[QuizOutcomeModel],
        algo_config: Dict[str, Any],
        special_rules: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        # 特殊规则优先
        special_code = self.check_special_rules(answers=answers, special_rules=special_rules)
        if special_code:
            special_outcome = next((o for o in outcomes if o.code == special_code), None)
            if special_outcome:
                return {"outcome_code": special_code, "score": None, "calc_result": {"triggered_by": "special_rule"}}

        dimensions = algo_config.get("dimensions", [])
        dim_codes = [d["code"] for d in sorted(dimensions, key=lambda x: x.get("sort_order", 0))]
        similarity_threshold = algo_config.get("similarity_threshold", 60)

        # Step1: 按维度汇总原始分（每维度2题，每题1-3分，总分2-6）
        dim_scores: Dict[str, int] = {code: 0 for code in dim_codes}
        for question in questions:
            if question.is_hidden:
                continue
            answer_key = answers.get(str(question.seq))
            if not answer_key:
                continue
            option = next((o for o in question.options if o.key == answer_key), None)
            if not option:
                continue
            for dim_code, score in (option.dim_scores or {}).items():
                if dim_code in dim_scores:
                    dim_scores[dim_code] += score

        # Step2: 归档 L/M/H → 1/2/3
        def archive(raw: int) -> int:
            if raw <= 3:
                return 1  # L
            elif raw == 4:
                return 2  # M
            else:
                return 3  # H

        user_vector = [archive(dim_scores.get(code, 2)) for code in dim_codes]

        # Step3: 曼哈顿距离匹配（排除特殊/兜底结果）
        normal_outcomes = [o for o in outcomes if not o.is_special and not o.is_fallback]
        fallback_outcome = next((o for o in outcomes if o.is_fallback), None)

        best_outcome = None
        best_distance = float("inf")
        best_exact_hits = -1

        max_possible_distance = len(dim_codes) * 2  # 每维度最大差值为2

        for outcome in normal_outcomes:
            dim_vector = outcome.match_config.get("dim_vector", []) if outcome.match_config else []
            if len(dim_vector) != len(user_vector):
                continue
            distance = sum(abs(u - t) for u, t in zip(user_vector, dim_vector))
            exact_hits = sum(1 for u, t in zip(user_vector, dim_vector) if u == t)
            if (distance < best_distance) or (distance == best_distance and exact_hits > best_exact_hits):
                best_distance = distance
                best_exact_hits = exact_hits
                best_outcome = outcome

        if not best_outcome:
            if fallback_outcome:
                return {"outcome_code": fallback_outcome.code, "score": 0, "calc_result": {"dim_scores": dim_scores, "dim_vector": user_vector}}
            raise BusinessError("未找到匹配的结果")

        # 计算相似度（百分比）
        similarity = int((1 - best_distance / max_possible_distance) * 100) if max_possible_distance > 0 else 100

        # 相似度不足则兜底
        if similarity < similarity_threshold and fallback_outcome:
            return {
                "outcome_code": fallback_outcome.code,
                "score": similarity,
                "calc_result": {"dim_scores": dim_scores, "dim_vector": user_vector},
            }

        return {
            "outcome_code": best_outcome.code,
            "score": similarity,
            "calc_result": {"dim_scores": dim_scores, "dim_vector": user_vector},
        }
