from db.conection import Base

class User(Base):
  __tablename__ = 'User'
  username: str
  email: str | None = None
  full_name: str | None = None
  disabled: bool | None = None
    
def fake_decode_token(token):
  return User(
    username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
  )