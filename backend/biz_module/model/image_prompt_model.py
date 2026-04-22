from typing import Optional
from pydantic import Field
from basic.model.basic_model import BasisModel


class ImagePromptConfig(BasisModel):
    """图像生成提示词配置，存为 JSONB"""
    prompt: str = Field(..., description="图像生成提示词（英文，适用于 SD/DALL-E 等模型）")
    style: Optional[str] = Field(None, description="风格标签，如 meme/anime/flat-design")
    negative_prompt: Optional[str] = Field(None, description="负面提示词")
