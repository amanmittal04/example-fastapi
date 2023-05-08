from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(
        **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/userProfile", response_model=schemas.UserProfile)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(
        models.User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    posts = [
        schemas.UserPost(title=post.title, content=post.content,
                         published=post.published, created_at=post.created_at).dict()
        for post in db.query(models.Post).filter(
            models.Post.owner_id == user.id
        ).all()
    ]
    return {"id": user.id, "email": user.email, "created_at": user.created_at, "phone_number": user.phone_number, "posts": posts}


@router.get("/notifications", response_model=List[schemas.Notification])
def get_notifications(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    notifications = db.query(models.Notification).filter(
        models.Notification.recipient_id == current_user.id).all()
    notifications_list = []
    for n in notifications:
        notifications_dict = {}
        notifications_dict["message"] = n.message
        notifications_list.append(notifications_dict)

    return notifications_list


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    return user
