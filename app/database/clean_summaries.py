
from app.database.db import SessionLocal
from app.database.models import TranscriptSummary

KEEP_FILES = {
    "Frontier_Springs_Ltd",
    "Millworks_Technologies_Ltd",
    "NIS_Management_Ltd"
}

db = SessionLocal()

try:
    records = db.query(TranscriptSummary).all()

    deleted = 0

    for record in records:
        if record.transcript_file not in KEEP_FILES:
            db.delete(record)
            deleted += 1

    db.commit()

    print("Database cleanup completed!")
    print("Old records deleted:", deleted)

    remaining = db.query(TranscriptSummary).all()

    print("\nRemaining companies:")

    for record in remaining:
        print("-", record.company_name)

finally:
    db.close()
