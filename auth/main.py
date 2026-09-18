
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.auth_db import get_db

# from auth.models import User
# import models, schemas, utils
from auth import models, schemas, utils

from jose import jwt 
from datetime import datetime, timedelta 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError



SECRET_KEY = "_1N_p6uBKzwqcbAQMg2s08XbX2TNlvWB6rdRkKowr2I"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# helper function that takes user data 
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db) ):
    # checks the user exit or not 
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail = "username already exist")


    # hashed the password 
    hashed_pass = utils.hash_password(user.password)

    # create new user instance 
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass,
        role=user.role
    )

    # save user to database 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    #Return the value excluding password 
    return {
            "id": new_user.id,
            "username": new_user.username, 
            "email": new_user.email,
            "role": new_user.role
            }


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login")), db: Session = Depends(get_db)):
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # user = db.query(models.User).filter(models.User.username == username).first()
    # if user is None:
    #     raise credentials_exception
    return {"username": username, "role": role}



@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! You have access to this protected route.", "role": current_user['role']}


def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user['role'] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
        return current_user
    return role_checker

@app.get("/profile")
def get_profile(current_user: dict = Depends(require_roles(["user", "admin"]))):  # Only users with role "user" or "admin" can access this route):
    return {"message": f"Profile of {current_user['username']}!", "role": current_user['role']}



@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_roles(["user"]))):  # Only users with role "user" can access this route
    return {"message": f"Welcome to the user dashboard, {current_user['username']}!", "role": current_user['role']}


@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):  # Only users with role "admin" can access this route
    return {"message": f"Welcome to the admin dashboard, {current_user['username']}!", "role": current_user['role']}









