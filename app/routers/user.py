from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, hashing, models, schemas

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserShow, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=404, detail="User with this email already exists")
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.bcrypt(request.password)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
