from fastapi import FastAPI , Depends , HTTPException
import crud, models, schemas
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal , engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/')
def root():
    return {"message" : "FASTAPI SERVER IS UP!!!"}

# @app.post('/users', response_model=schemas.User)
# def create_user(user : schemas.UserCreate , db:Session = Depends(get_db)):
#     pass



@app.post('/users', response_model=schemas.User)
def create_user(user : schemas.UserCreate , db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    return crud.create_user(db, user)

@app.get('/users', response_model=List[schemas.User])
def get_users(skip:int = 0 ,limit:int=100,  db:Session = Depends(get_db)):
    db_users = crud.get_users(db, skip, limit)
    return db_users

@app.get('/users/{user_id}', response_model=schemas.User)
def get_user(user_id :int , db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="User Not Found!")
    return db_user

@app.post('/users/{user_id}/posts/', response_model=schemas.Post)
def create_user_post(user_id:int , post : schemas.PostCreate , db:Session = Depends(get_db)):
    return crud.create_user_post(db, post,user_id)

@app.get('/users/{user_id}/posts/', response_model=List[schemas.Post])
def get_user_posts(user_id: int , db:Session = Depends(get_db)):
    return crud.get_user_posts(db, user_id)
    

@app.delete('/users/{user_id}/posts/{blog_id}')
def delete_user_post(user_id:int , blog_id:int, db:Session = Depends(get_db)):
    return crud.delete_user_blog(db , user_id, blog_id)

@app.patch('/users/{user_id}/posts/{blog_id}', response_model=schemas.Post)
def update_user_post(user_id: int ,blog_id:int,post : schemas.PostCreate , db:Session = Depends(get_db)):
    return crud.update_user_blog(db,post, user_id, blog_id)

@app.get('/posts', response_model=List[schemas.Post])
def get_all_posts(skip:int = 0 ,limit:int=100, db:Session = Depends(get_db)):
    return crud.get_posts(db, skip, limit)




