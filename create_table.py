from database import Base, engine
import model 



# / caling sqlalchemy to create the tables in the database
# telling sql alchmey to create all the tables mentioned in model.py file 
# in the database if they do not exist already
Base.metadata.create_all(bind=engine)





