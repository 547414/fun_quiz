from typing import Optional, List, Dict, Any
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic_module.model.upload_model import UploadResModel
from biz_module.model.image_prompt_model import ImagePromptConfig


class QuizOutcomeModel(BasicVersionModel):
    quiz_id: str = Field(..., description="所属测验ID")
    code: str = Field(..., description="结果编码")
    name: str = Field(..., description="结果名称")
    avatar: Optional[UploadResModel] = Field(None, description="结果形象图文件JSON")
    avatar_prompt: Optional[ImagePromptConfig] = Field(None, description="结果头像生成提示词")
    summary: Optional[str] = Field(None, description="简短描述")
    detail: Optional[str] = Field(None, description="详细解读文案")
    tags: Optional[List[str]] = Field(None, description="特征标签")
    sort_order: int = Field(0, description="排序")
    is_fallback: bool = Field(False, description="是否为兜底结果")
    is_special: bool = Field(False, description="是否为特殊触发结果")
    match_config: Optional[Dict[str, Any]] = Field(None, description="匹配条件JSON")


class EditQuizOutcomeParamsModel(QuizOutcomeModel):
    quiz_id: Optional[str] = Field(None, description="所属测验ID")
    code: Optional[str] = Field(None, description="结果编码")
    name: Optional[str] = Field(None, description="结果名称")
    avatar_prompt: Optional[ImagePromptConfig] = Field(None, description="结果头像生成提示词")

    def to_outcome_model(self) -> QuizOutcomeModel:
        return QuizOutcomeModel(
            id=self.id,
            version=self.version,
            operator=self.operator,
            operator_category=self.operator_category,
            created_at=self.created_at,
            updated_at=self.updated_at,
            quiz_id=self.quiz_id,
            code=self.code,
            name=self.name,
            avatar=self.avatar,
            avatar_prompt=self.avatar_prompt,
            summary=self.summary,
            detail=self.detail,
            tags=self.tags,
            sort_order=self.sort_order,
            is_fallback=self.is_fallback,
            is_special=self.is_special,
            match_config=self.match_config,
        )


class DeleteQuizOutcomeParamsModel(BasisModel):
    outcome_id: str = Field(..., description="结果ID")


class BatchSaveOutcomesParamsModel(BasisModel):
    quiz_id: str = Field(..., description="测验ID")
    outcomes: List[EditQuizOutcomeParamsModel] = Field(..., description="结果列表（全量替换）")
