from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    project_name: Optional[str] = None
    pr_number: Optional[str] = None
    issue_number: Optional[str] = None
