from typing import List, Dict, Optional

from pydantic import Field

from basic.model.basic_model import BasisModel


class CaptchaTextPositionDetailModel(BasisModel):
    x: int = Field(..., description="x坐标")
    y: int = Field(..., description="y坐标")


class CaptchaTextPositionModel(BasisModel):
    text: Optional[str] = Field(None, description="验证码文本")
    pinyin: Optional[str] = Field(None, description="拼音")
    top_left: CaptchaTextPositionDetailModel = Field(..., description="左上角坐标")
    bottom_right: CaptchaTextPositionDetailModel = Field(..., description="右下角坐标")


class CaptchaModel(BasisModel):
    captcha_id: str = Field(..., description="验证码ID")
    correct_texts: List[str] = Field(..., description="正确文本")
    text_positions: Dict[str, CaptchaTextPositionModel] = Field(..., description="文本位置")


class CaptchaViewModel(BasisModel):
    captcha_id: str = Field(..., description="验证码ID")
    correct_texts: List[str] = Field(..., description="正确文本")
    correct_pinyin_texts: List[str] = Field(..., description="正确文本")
    captcha_base64: str = Field(..., description="验证码base64")


class CaptchaValidatePositionParamsModel(BasisModel):
    text: str = Field(..., description="验证码文本")
    x: int = Field(..., description="x坐标")
    y: int = Field(..., description="y坐标")


class CaptchaValidateParamsModel(BasisModel):
    captcha_id: str = Field(..., description="验证码ID")
    text_positions: List[CaptchaValidatePositionParamsModel] = Field(..., description="验证码文本位置")
