import csv
from src.database.db import SessionLocal
from src.database.models.part import Part

def import_parts():
    db = SessionLocal()

    with open("vin_parts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            part = Part(
                vin=row["vin"],
                brand=row["brand"],
                model=row["model"],
                year=int(row["year"]),
                engine=row["engine"],
                category=row["category"],
                sub_category=row["sub_category"],
                part_number=row["part_number"],
                part_name=row["part_name"],
                oem=row["oem"].lower() == "true"
            )

            db.add(part)

        db.commit()
        db.close()

    print("Импорт завершён!")

if __name__ == "__main__":
    import_parts()
