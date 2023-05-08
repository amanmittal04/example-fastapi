from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserPost(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime

    def dict(self, **kwargs):
        return {
            "title": self.title,
            "content": self.content,
            "published": self.published,
            "created_at": self.created_at
        }

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    created_at: datetime
    posts: List[UserPost]

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class Notification(BaseModel):
    message: str
