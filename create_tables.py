from config.database import Base, engine


# Models
from app.users import models
from app.vacancies import models
from app.skills import models


def create_tables():
    print("Creating database and tables...")
    Base.metadata.create_all(engine)
    print("Done!")


def main():
    try:
        create_tables()
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
