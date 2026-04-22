from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import Field
from basic.model.basic_model import BasisModel, BasicModel, BasicVersionModel


class QuizTokenModel(BasicVersionModel):
    token: str = Field(..., description="访问令牌")
    status: str = Field("active", description="状态: active/exhausted/expired")
    max_uses: Optional[int] = Field(None, description="最大使用次数，NULL表示不限")
    used_count: int = Field(0, description="已使用次数")
    source: str = Field("admin", description="来源: purchase/gift/admin/batch")
    batch_code: Optional[str] = Field(None, description="批次编码")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    extra: Optional[Dict[str, Any]] = Field(None, description="扩展信息JSON")


class GenerateTokenParamsModel(BasisModel):
    count: int = Field(1, description="生成数量", ge=1, le=1000)
    max_uses: Optional[int] = Field(None, description="每个token可用次数，NULL表示不限")
    source: str = Field("admin", description="来源")
    batch_code: Optional[str] = Field(None, description="批次编码")
    expires_at: Optional[datetime] = Field(None, description="过期时间，NULL表示永不过期")
    quiz_ids: Optional[List[str]] = Field(None, description="授权测验ID列表，空表示不限制")
    extra: Optional[Dict[str, Any]] = Field(None, description="扩展信息")


class TokenListParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="每页数量")
    batch_code: Optional[str] = Field(None, description="批次筛选")
    status: Optional[str] = Field(None, description="状态筛选")


class ValidateTokenParamsModel(BasisModel):
    token: str = Field(..., description="访问令牌")


class TokenDetailViewModel(QuizTokenModel):
    quiz_ids: Optional[List[str]] = Field(None, description="授权测验ID列表")


class GeneratedTokensViewModel(BasisModel):
    tokens: list = Field(..., description="生成的token列表")
    batch_code: str = Field(..., description="批次编码")
    count: int = Field(..., description="实际生成数量")


class QuizTokenQuizModel(BasicModel):
    token_id: str = Field(..., description="Token ID")
    quiz_id: str = Field(..., description="测验 ID")


class UpdateTokenQuizIdsModel(BasisModel):
    token_id: str = Field(..., description="Token ID")
    quiz_ids: Optional[List[str]] = Field(None, description="授权测验ID列表，空或null表示不限制")
