from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
import datetime
from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from pytz import utc
import smtplib
from .sendEmail import send_email


scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


def create_notification(db: Session, sender_id: int, recipient_id: int, message: str):
    notification = models.Notification(
        sender_id=sender_id,
        recipient_id=recipient_id,
        message=message,
    )
    db.add(notification)
    db.commit()


def scan_user_posts(user_id, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(
        models.Post.owner_id == user_id).all()
    # user = db.query(models.User).filter(models.User.id == user_id).first()
    # print(user['email'])
    current_time = datetime.now().date()

    for post in posts:
        created_time = post.created_at
        expiration_time = post.expiration_time
        if current_time == (created_time + timedelta(days=expiration_time)).date():
            message = f"Your Post with title : {post.title} has expired"
            create_notification(db, user_id, user_id, message)
            post_query = db.query(models.Post).filter(
                models.Post.id == post.id)
            post = post_query.first()
            if post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with id: {id} not found")

            if post.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not Authorized to perform requested action")

            post_query.delete(synchronize_session=False)
            db.commit()


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
    scheduler.add_job(scan_user_posts, 'interval',
                      minutes=1, args=[current_user.id, db])
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
async def get_notifications(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    await send_email("divinityworld04@gmail.com", "post expired", "Post Expired")
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
