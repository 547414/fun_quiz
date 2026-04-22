from pydantic import Field
from basic.model.basic_model import BasicVersionModel


class WebUserOrganizationModel(BasicVersionModel):
    web_user_id: str = Field(..., description="web用户id")
    organization_id: str = Field(..., description="组织id")
