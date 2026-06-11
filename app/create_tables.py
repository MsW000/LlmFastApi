from database import engine, Base
from models import Message

Base.metadata.create_all(bind=engine)\

print("Таблицы созданы")