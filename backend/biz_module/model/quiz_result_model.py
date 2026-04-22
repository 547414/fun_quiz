from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic_module.model.upload_model import UploadResModel


class OutcomeDistributionModel(BasisModel):
    outcome_code: str = Field(..., description="结果编码")
    outcome_name: Optional[str] = Field(None, description="结果名称")
    cnt: int = Field(0, description="数量")


class QuizResultModel(BasicVersionModel):
    token_id: str = Field(..., description="访问令牌ID")
    quiz_id: str = Field(..., description="所属测验ID")
    answers: Dict[str, str] = Field(..., description="原始答案 {question_seq: option_key}")
    calc_result: Optional[Dict[str, Any]] = Field(None, description="计算中间结果JSON")
    outcome_code: str = Field(..., description="命中结果编码")
    outcome_id: str = Field(..., description="命中结果ID")
    score: Optional[int] = Field(None, description="匹配度（百分比）")
    share_image: Optional[UploadResModel] = Field(None, description="分享图文件JSON")


class QuizTokenBody(BasisModel):
    token: Optional[str] = Field(None, description="测验访问令牌")


class SubmitAnswersParamsModel(BasisModel):
    token: Optional[str] = Field(None, description="测验访问令牌")
    answers: Dict[str, str] = Field(..., description="答案 {question_seq: option_key}")


class QuizResultViewModel(BasisModel):
    result_id: str = Field(..., description="结果ID")
    quiz_id: str = Field(..., description="测验ID")
    quiz_name: str = Field(..., description="测验名称")
    quiz_type: str = Field(..., description="测验类型")
    outcome_code: str = Field(..., description="结果编码")
    outcome_name: str = Field(..., description="结果名称")
    outcome_summary: Optional[str] = Field(None, description="结果简短描述")
    outcome_detail: Optional[str] = Field(None, description="结果详细解读")
    outcome_tags: Optional[List[str]] = Field(None, description="特征标签")
    outcome_avatar: Optional[UploadResModel] = Field(None, description="结果形象图")
    score: Optional[int] = Field(None, description="匹配度")
    calc_result: Optional[Dict[str, Any]] = Field(None, description="计算中间结果（供展示雷达图等）")
    share_image: Optional[UploadResModel] = Field(None, description="分享图文件JSON")
    result_config: Optional[Dict[str, Any]] = Field(None, description="结果页展示配置")


class QuizPlayOptionModel(BasisModel):
    key: str = Field(..., description="选项键")
    label: str = Field(..., description="选项文案")
    images: Optional[List[UploadResModel]] = Field(None, description="选项图片")
    next_question_seq: Optional[int] = Field(None, description="下一题序号（branch类型）")


class QuizPlayQuestionModel(BasisModel):
    seq: int = Field(..., description="题目序号")
    content: str = Field(..., description="题目内容")
    images: Optional[List[UploadResModel]] = Field(None, description="题目图片")
    is_hidden: bool = Field(False, description="是否隐藏判定题")
    options: List[QuizPlayOptionModel] = Field(..., description="选项列表")
    branch_config: Optional[Dict[str, Any]] = Field(None, description="分支配置")


class QuizPlayViewModel(BasisModel):
    """移动端答题所需数据"""
    quiz_id: str = Field(..., description="测验ID")
    quiz_name: str = Field(..., description="测验名称")
    quiz_type: str = Field(..., description="测验类型")
    covers: Optional[List[UploadResModel]] = Field(None, description="封面图列表")
    share_title: Optional[str] = Field(None, description="分享标题")
    questions: List[QuizPlayQuestionModel] = Field(..., description="题目列表")
    algo_config: Optional[Dict[str, Any]] = Field(None, description="供前端使用的算法配置（branch类型需要）")
    result_config: Optional[Dict[str, Any]] = Field(None, description="结果页展示配置")


class HistoryItemViewModel(BasisModel):
    """历史答题记录（用于列表展示）"""
    result_id: str = Field(..., description="结果ID")
    quiz_id: str = Field(..., description="测验ID")
    quiz_name: str = Field(..., description="测验名称")
    quiz_type: str = Field(..., description="测验类型")
    outcome_code: str = Field(..., description="结果编码")
    outcome_name: str = Field(..., description="结果名称")
    outcome_summary: Optional[str] = Field(None, description="结果简介")
    outcome_avatar: Optional[UploadResModel] = Field(None, description="结果形象图")
    score: Optional[int] = Field(None, description="匹配度")
    created_at: Optional[datetime] = Field(None, description="答题时间")


class TokenEntryViewModel(BasisModel):
    """移动端入口数据：token状态"""
    status: str = Field(..., description="token状态: active/exhausted/expired")
    max_uses: Optional[int] = Field(None, description="最大使用次数，NULL表示不限")
    used_count: int = Field(0, description="已使用次数")
    has_history: bool = Field(False, description="是否存在历史记录")
