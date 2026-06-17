from app.db.database import Base, engine
from .models import *

Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente")