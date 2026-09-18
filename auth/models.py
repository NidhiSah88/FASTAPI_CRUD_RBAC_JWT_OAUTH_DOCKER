
# cat > auth/create_auth_table.py <<'EOF'
from sqlalchemy import Column, Integer, String, Text, Date
from auth.auth_db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # Default role is "user"

print("Tables created successfully in models py file!")
# EOF

# from auth.auth_db import Base, engine
# from auth import models

# print("Registered tables:", Base.metadata.tables.keys())

# Base.metadata.create_all(bind=engine)

# print("Tables created successfully in modelspy file!")


