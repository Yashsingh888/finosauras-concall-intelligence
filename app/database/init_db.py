
from app.database.db import engine, Base
from app.database import models


def initialize_database():

    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully!")
    print("Tables created:")
    print("- announcements")
    print("- transcript_summaries")


if __name__ == "__main__":
    initialize_database()
