from typing import Optional, List, Dict, Any
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicVersionModel
from basic_module.model.upload_model import UploadResModel
from biz_module.model.image_prompt_model import ImagePromptConfig


class QuizOptionModel(BasisModel):
    key: str = Field(..., description="选项键")
    label: str = Field(..., description="选项文案")
    images: Optional[List[UploadResModel]] = Field(None, description="选项图片")
    image_prompt: Optional[ImagePromptConfig] = Field(None, description="选项图片生成提示词")
    dim_scores: Optional[Dict[str, int]] = Field(None, description="各维度得分（vector类型）")
    score: Optional[int] = Field(None, description="分值（score/random类型）")
    next_question_seq: Optional[int] = Field(None, description="下一题序号（branch类型）")
    outcome_code: Optional[str] = Field(None, description="结果编码（branch终止选项）")


class QuizQuestionModel(BasicVersionModel):
    quiz_id: str = Field(..., description="所属测验ID")
    seq: int = Field(..., description="题目序号")
    content: str = Field(..., description="题目内容")
    images: Optional[List[UploadResModel]] = Field(None, description="题目配图文件列表JSON")
    image_prompt: Optional[ImagePromptConfig] = Field(None, description="题目图片生成提示词")
    is_hidden: bool = Field(False, description="是否隐藏判定题")
    options: List[QuizOptionModel] = Field(..., description="选项配置JSON")
    branch_config: Optional[Dict[str, Any]] = Field(None, description="分支配置JSON")


class EditQuizQuestionParamsModel(QuizQuestionModel):
    quiz_id: Optional[str] = Field(None, description="所属测验ID")
    seq: Optional[int] = Field(None, description="题目序号")
    content: Optional[str] = Field(None, description="题目内容")
    images: Optional[List[UploadResModel]] = Field(None, description="题目配图文件列表JSON")
    image_prompt: Optional[ImagePromptConfig] = Field(None, description="题目图片生成提示词")
    options: Optional[List[QuizOptionModel]] = Field(None, description="选项配置JSON")

    def to_question_model(self) -> QuizQuestionModel:
        return QuizQuestionModel(
            id=self.id,
            version=self.version,
            operator=self.operator,
            operator_category=self.operator_category,
            created_at=self.created_at,
            updated_at=self.updated_at,
            quiz_id=self.quiz_id,
            seq=self.seq,
            content=self.content,
            images=self.images,
            image_prompt=self.image_prompt,
            is_hidden=self.is_hidden,
            options=self.options,
            branch_config=self.branch_config,
        )


class DeleteQuizQuestionParamsModel(BasisModel):
    question_id: str = Field(..., description="题目ID")


class BatchSaveQuestionsParamsModel(BasisModel):
    quiz_id: str = Field(..., description="测验ID")
    questions: List[EditQuizQuestionParamsModel] = Field(..., description="题目列表（全量替换）")
