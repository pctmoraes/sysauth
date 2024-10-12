from pydantic import BaseModel


class MfaSchema(BaseModel):
    user_id: int
    app: str
    username: str
