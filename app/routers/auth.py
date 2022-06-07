from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, utils, models, oauth2
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def Login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid ceadential"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid ceadential"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
