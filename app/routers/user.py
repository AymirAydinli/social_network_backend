from app.utils import pwd_hash
from app import schemas, models, oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["Users"])


@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserModel, db: Session = Depends(get_db)):

    # hash the password - user.password
    user.password = pwd_hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"user with id {id} does not exist",
        )
    return user


@router.get("/users", response_model=list[schemas.UserModel])
def get_all_users(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):

    users = db.query(models.User).all()
    return users
