from sqlite3 import Connection
from typing import List
from src.model.models import Company


class CompanyRepository:
    db: Connection

    def __init__(self, db):
        self.db = db

    def fetch_columns(self):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA table_info(company)")
        return [column[1] for column in cursor.fetchall()]

    def delete_all(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM company")
        self.db.commit()

    def create_company(self, company: Company):
        cursor = self.db.cursor()

        cursor.execute(
            "INSERT INTO company(name, block1_slots, block2_slots, capacity) VALUES($1, $2, $3, $4)",
            [
                company.name,
                str(company.slots["block1"]),
                str(company.slots["block2"]),
                company.capacity,
            ],
        )
        self.db.commit()

    def get_all_companies(self) -> List[Company]:
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM company")

        result = cursor.fetchall()

        return list(map(lambda item: Company.from_row(item), result))

    def get_company_by_name(self, name: str) -> Company:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM company WHERE name=$1", [name])
        result = cursor.fetchall()
        return Company.from_row(result[0])

    def delete(self, name: str):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM company WHERE name=$1", [name])
        self.db.commit()

    def get_company_by_id(self, id: str) -> Company:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM company WHERE id=$1", [id])
        result = cursor.fetchall()
        return Company.from_row(result[0])
