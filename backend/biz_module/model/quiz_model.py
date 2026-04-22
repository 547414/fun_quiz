from typing import Optional, List, Dict, Any
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic_module.model.upload_model import UploadResModel
from biz_module.model.image_prompt_model import ImagePromptConfig


class QuizModel(BasicVersionModel):
    name: str = Field(..., description="测验名称")
    code: str = Field(..., description="测验编码")
    covers: Optional[List[UploadResModel]] = Field(None, description="封面图文件列表JSON")
    cover_prompt: Optional[ImagePromptConfig] = Field(None, description="封面图生成提示词")
    quiz_type: str = Field("vector", description="测验类型")
    status: str = Field("draft", description="状态")
    source: str = Field("manual", description="来源")
    sort_order: int = Field(0, description="排序")
    share_title: Optional[str] = Field(None, description="分享标题")
    share_desc: Optional[str] = Field(None, description="分享描述")
    fallback_outcome_code: Optional[str] = Field(None, description="兜底结果编码")
    algo_config: Optional[Dict[str, Any]] = Field(None, description="算法配置JSON")
    special_rules: Optional[List[Dict[str, Any]]] = Field(None, description="特殊判定规则JSON")
    result_config: Optional[Dict[str, Any]] = Field(None, description="结果页展示配置JSON")


class PublishedQuizModel(BasisModel):
    """入口页用：已发布测验列表轻量视图"""
    id: str = Field(..., description="测验ID")
    name: str = Field(..., description="测验名称")
    quiz_type: str = Field(..., description="测验类型")
    covers: Optional[List[UploadResModel]] = Field(None, description="封面图列表")
    share_title: Optional[str] = Field(None, description="分享标题")
    share_desc: Optional[str] = Field(None, description="分享描述")


class QuizViewModel(QuizModel):
    question_count: Optional[int] = Field(None, description="题目数量")
    outcome_count: Optional[int] = Field(None, description="结果数量")
    participate_count: Optional[int] = Field(None, description="参与次数")


class QuizListParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="每页数量")
    search: Optional[str] = Field(None, description="搜索关键词")
    quiz_type: Optional[str] = Field(None, description="测验类型筛选")
    status: Optional[str] = Field(None, description="状态筛选")


class EditQuizParamsModel(QuizModel):
    name: Optional[str] = Field(None, description="测验名称")
    code: Optional[str] = Field(None, description="测验编码")

    def to_quiz_model(self) -> QuizModel:
        return QuizModel(
            id=self.id,
            version=self.version,
            operator=self.operator,
            operator_category=self.operator_category,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            code=self.code,
            covers=self.covers,
            cover_prompt=self.cover_prompt,
            quiz_type=self.quiz_type,
            status=self.status,
            source=self.source,
            sort_order=self.sort_order,
            share_title=self.share_title,
            share_desc=self.share_desc,
            fallback_outcome_code=self.fallback_outcome_code,
            algo_config=self.algo_config,
            special_rules=self.special_rules,
            result_config=self.result_config,
        )


class DeleteQuizParamsModel(BasisModel):
    quiz_id: str = Field(..., description="测验ID")


class PublishQuizParamsModel(BasisModel):
    quiz_id: str = Field(..., description="测验ID")
    status: str = Field(..., description="目标状态: published/archived/draft")


class ImportQuizParamsModel(BasisModel):
    definition: Dict[str, Any] = Field(..., description="Quiz Definition JSON（见SKILL.md）")


class QuizStatsModel(BasisModel):
    quiz_id: str = Field(..., description="测验ID")
    quiz_name: str = Field(..., description="测验名称")
    total_tokens: int = Field(0, description="Token总数")
    used_tokens: int = Field(0, description="已使用Token数")
    outcome_distribution: Optional[List[Dict[str, Any]]] = Field(None, description="结果分布")
