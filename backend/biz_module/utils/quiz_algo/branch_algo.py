from typing import Dict, Any, List
from basic.error.base_error import BusinessError
from biz_module.model.quiz_question_model import QuizQuestionModel
from biz_module.model.quiz_outcome_model import QuizOutcomeModel
from biz_module.utils.quiz_algo.base import BaseQuizAlgo


class BranchAlgo(BaseQuizAlgo):
    """
    分支跳题算法（决策树）
    根据答案沿题目跳转链路，到达 next_question_seq=-1 的终止节点，取 outcome_code
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

        question_map: Dict[int, QuizQuestionModel] = {q.seq: q for q in questions}

        current_seq = 1
        path = [current_seq]
        outcome_code = None
        max_steps = len(questions) + 5  # 防止死循环

        for _ in range(max_steps):
            question = question_map.get(current_seq)
            if not question:
                break
            answer_key = answers.get(str(current_seq))
            if not answer_key:
                break
            option = next((o for o in question.options if o.key == answer_key), None)
            if not option:
                break

            next_seq = option.next_question_seq
            if next_seq == -1:
                outcome_code = option.outcome_code
                break

            current_seq = next_seq
            path.append(current_seq)

        if not outcome_code:
            fallback = next((o for o in outcomes if o.is_fallback), None)
            if fallback:
                return {"outcome_code": fallback.code, "score": None, "calc_result": {"path": path}}
            raise BusinessError("分支路径未到达终止节点")

        return {
            "outcome_code": outcome_code,
            "score": None,
            "calc_result": {"path": path},
        }
