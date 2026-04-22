from abc import ABC, abstractmethod
from typing import Dict, Any, List
from biz_module.model.quiz_question_model import QuizQuestionModel
from biz_module.model.quiz_outcome_model import QuizOutcomeModel


class BaseQuizAlgo(ABC):
    """测验算法基类，所有类型的算法策略继承此类"""

    @abstractmethod
    def calculate(
        self,
        answers: Dict[str, str],
        questions: List[QuizQuestionModel],
        outcomes: List[QuizOutcomeModel],
        algo_config: Dict[str, Any],
        special_rules: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        执行算法计算，返回：
        {
            outcome_code: str,     # 命中结果编码
            score: int | None,     # 匹配度（百分比），不适用则为None
            calc_result: dict,     # 中间计算产物
        }
        """
        pass

    def check_special_rules(
        self,
        answers: Dict[str, str],
        special_rules: List[Dict[str, Any]],
    ) -> str | None:
        """检查特殊规则，命中则返回 outcome_code，否则返回 None"""
        if not special_rules:
            return None
        for rule in special_rules:
            condition_type = rule.get("condition_type")
            if condition_type == "option_selected":
                question_seq = str(rule.get("question_seq"))
                option_key = rule.get("option_key")
                if answers.get(question_seq) == option_key:
                    return rule.get("trigger_outcome_code")
        return None
