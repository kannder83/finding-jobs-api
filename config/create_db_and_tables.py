from config.database import Base, engine


# Models
from app.users import models
from app.skills import models


def create_tables():
    print("Creating database and tables...")

    Base.metadata.create_all(engine)
