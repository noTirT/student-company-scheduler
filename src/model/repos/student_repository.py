from sqlite3 import Connection
from typing import List
from src.model.models import Student


class StudentRepository:
    db: Connection

    def __init__(self, db):
        self.db = db

    def fetch_columns(self):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA table_info(student)")
        return [column[1] for column in cursor.fetchall()]

    def delete_all(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM student")
        self.db.commit()

    def create_student(self, student: Student):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO student(name, grade) VALUES($name, $grade)",
            {"name": student.name, "grade": student.grade},
        )
        self.db.commit()

    def get_student_by_name(self, name: str) -> Student:
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM student WHERE name=$1", [name])

        result = cursor.fetchall()

        return Student.from_row(result[0])

    def get_all_students(self) -> List[Student]:
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM student")

        result = cursor.fetchall()

        return list(map(lambda item: Student.from_row(item), result))

    def get_students_by_grade(self, grade: str) -> List[Student]:
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM student WHERE grade=$1", [grade])

        result = cursor.fetchall()

        return list(map(lambda item: Student.from_row(item), result))

    def get_student_by_id(self, id: str) -> Student:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM student WHERE id=$1", [id])
        result = cursor.fetchall()
        return Student.from_row(result[0])

    def delete_student(self, name: str):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM student WHERE name=$1", [name])
        self.db.commit()

    def get_students_without_selection(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM student WHERE id NOT IN(SELECT student_id FROM student_selection)"
        )
        result = cursor.fetchall()
        return list(map(lambda item: Student.from_row(item), result))

    def get_students_with_selection(self):
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM student WHERE id IN(SELECT student_id FROM student_selection)"
        )
        result = cursor.fetchall()
        return list(map(lambda item: Student.from_row(item), result))

    def get_available_grades(self) -> list[str]:
        cursor = self.db.cursor()
        cursor.execute("SELECT grade FROM student")
        result = cursor.fetchall()
        return list(map(lambda item: item[0], result))
