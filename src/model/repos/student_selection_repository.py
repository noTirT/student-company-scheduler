from sqlite3 import Connection
from typing import List

from src.model.models import StudentSelection


class StudentSelectionRepository:
    db: Connection

    def __init__(self, db: Connection) -> None:
        self.db = db

    def fetch_columns(self):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA table_info(student_selection)")
        return [column[1] for column in cursor.fetchall()]

    def delete_all(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM student_selection")
        self.db.commit()

    def create_student_selection(
        self, student_id: int, company_id: int, block: int, slot: int
    ):
        cursor = self.db.cursor()

        cursor.execute(
            "INSERT INTO student_selection(student_id, company_id, block, slot) VALUES($1, $2, $3, $4)",
            [student_id, company_id, block, slot],
        )
        self.db.commit()

    def get_student_selections_by_student_id(
        self, student_id: int
    ) -> List[StudentSelection]:
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM student_selection WHERE student_id=$1", [student_id]
        )

        result = cursor.fetchall()

        return list(map(lambda item: StudentSelection.from_row(item), result))

    def get_all_selections_ordered(self) -> List[StudentSelection]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM student_selection ORDER BY block,slot")
        result = cursor.fetchall()

        return list(map(lambda item: StudentSelection.from_row(item), result))

    def delete_selection_by_student_name(self, name: str):
        cursor = self.db.cursor()
        cursor.execute(
            "DELETE FROM student_selection WHERE student_id IN (SELECT id FROM student WHERE name=$1)",
            [name],
        )
        self.db.commit()
