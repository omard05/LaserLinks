import csv
from pathlib import Path

from sqlalchemy import select

from database import SessionLocal
from models import Course

CSV_PATH = Path(__file__).parent / "data" / "courses.csv"


def seed_courses():
    db = SessionLocal()
    added = 0
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                exists = db.scalar(
                    select(Course).where(
                        Course.subject == row["subject"],
                        Course.number == row["number"],
                        Course.term == row["term"],
                    )
                )
                if exists:
                    continue
                db.add(Course(**row))
                added += 1
        db.commit()
    finally:
        db.close()
    print(f"Added {added} courses")


if __name__ == "__main__":
    seed_courses()