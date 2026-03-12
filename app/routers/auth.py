from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, aouth2 # Ensure this matches your filename

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token) # Add the response model
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # OAuth2PasswordRequestForm uses .username for the email field
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Verify the password using the function we added to utils.py
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Create the token
    access_token = aouth2.create_access_token(data={"user_id": user.id})
    
    # Return the dictionary matching your schemas.Token (accessToken and tokenType)
    return {"accessToken": access_token, "tokenType": "bearer"}


  