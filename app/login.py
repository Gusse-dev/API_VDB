from fastapi import APIRouter, status
from .schemas import Token

from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException

from .user_managent import authenticate_user, create_access_token



router_login = APIRouter(prefix='/auth')


@router_login.post("/token", 
                    response_model=Token,
                    summary="Login into the user system",
                    description="Login with username and password. In case of successful login a authorization token is returned..",
                    response_description="Login Successful - Access to user specific documents granted",
                    status_code=status.HTTP_200_OK,
                    responses={
                            status.HTTP_400_BAD_REQUEST: {"description": "Bad request - Login unsuccessful","content": {"application/json": {"example": {"detail": "Username or password is incorrect"}}}},
                            },
                   )
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
