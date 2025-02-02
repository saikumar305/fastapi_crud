from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_item = models.Post(**post.model_dump(), author_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_posts(db:Session , user_id: int):
    return db.query(models.Post).filter(models.Post.author_id == user_id).all()


def delete_user_blog(db:Session , user_id:int , blog_id:int):
    db_item = db.query(models.Post).filter(models.Post.author_id == user_id and models.Post.id == blog_id).first()
    if not db_item:
        return {
            "records": [], 
            "message" : "No record found"
        }
    res = db.delete(db_item)
    db.commit()
    return res


def update_user_blog(db:Session , post: schemas.PostCreate , user_id:int , blog_id:int):
    db_item = db.query(models.Post).filter(models.Post.author_id == user_id and models.Post.id == blog_id).first()

    if post.title:
        db_item.title = post.title 
    db_item.description = post.description

    db.commit()
    db.refresh(db_item)

    return db_item



