
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

# // for docker compose file 
import os

# // without docker compose file
MYSQL_USER = "root"
MYSQL_PASSWORD = "" 
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "fastapi_crud"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


#connection to the database
engine = create_engine(DATABASE_URL,) 


#  values come from  docker compose file , 
# if value not present then it takes 2nd argument as default value like "root" for MYSQL_USER, "" for MYSQL_PASSWORD, "localhost" for MYSQL_HOST, 3306 for MYSQL_PORT and "fastapi_crud" for MYSQL_DATABASE
# MYSQL_USER = os.getenv("MYSQL_USER", "root")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "") 
# MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
# MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
# MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fastapi_crud")



# DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

#connection to the database
# engine = create_engine(DATABASE_URL,
#                        echo=True, pool_pre_ping=True)

# session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
    

## Base 
Base = declarative_base()













