from pydantic import Field
from basic.model.basic_model import BasicVersionModel


class WebUserDeptModel(BasicVersionModel):
    web_user_id: str = Field(..., description="web用户ID")
    dept_id: str = Field(..., description="部门ID")
