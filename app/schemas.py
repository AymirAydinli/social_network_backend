from pydantic import BaseModel, EmailStr, ConfigDict, conint, field_validator
from datetime import datetime
from typing import Optional, Any


class UserModel(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # model_config = ConfigDict(coerce_numbers_to_str=True)

    id: int  # Optional[str] = None


class VoteOut(BaseModel):
    post_id: int
    dir: int

    @field_validator("dir")
    def check(cls, v: Any) -> Any:
        if v not in (0, 1):
            raise ValueError("dir must be 0 or 1")
        return v


class PostBase(BaseModel):

    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Posts: PostResponse
    votes: int

    class Config:
        from_attributes = True
