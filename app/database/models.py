
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database.db import Base


class Announcement(Base):

    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255), nullable=False)

    exchange = Column(String(10))

    subject = Column(String(500))

    pdf_url = Column(Text, unique=True)

    status = Column(
        String(50),
        default="pending"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class TranscriptSummary(Base):

    __tablename__ = "transcript_summaries"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255), nullable=False)

    transcript_file = Column(String(500))

    summary_json = Column(Text)

    summary_markdown = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
