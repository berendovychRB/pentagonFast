from fastapi import FastAPI, Depends, status, Response, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
import datetime
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create', status_code=status.HTTP_201_CREATED )
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(email=request.email,
                           name=request.name,
                           hashed_password=request.hashed_password,
                           is_admin=request.is_admin)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Method is needed to fix updated_at Field
@app.put('/user/{id}/update', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} is not found')

    user.update(request)
    db.commit()

    return 'Successful Updated'


@app.get('/users')
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', status_code=200)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'User with the id {id} is not available'}
    return user


@app.delete('/user/{id}', responses={204: {'model': None}})
def delete_user(id, db: Session = Depends(get_db)):    # if status=status.HTTP_204 use, will be error ( bug in FastAPI )
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return 'Successful Deleted'


@app.get('/')
def hello():
    return {'data': 'Hello world'}















