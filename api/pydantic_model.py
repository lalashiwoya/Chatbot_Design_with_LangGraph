from pydantic import BaseModel

class UserSettings(BaseModel):
    llm_model_name: str = "gpt-3.5-turbo"