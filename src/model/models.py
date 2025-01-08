from sqlite3 import Row
from typing import Any, List
import ast


class DatabaseModel:
    @staticmethod
    def from_row(db_row: Row) -> Any:
        return

    def to_table_row(self) -> List[Any]:
        return []


class StudentSelection(DatabaseModel):
    student_id: int
    company_id: int
    block: int
    slot: int

    def __init__(self, student_id: int, company_id: int, block: int, slot: int) -> None:
        self.student_id = student_id
        self.company_id = company_id
        self.block = block
        self.slot = slot

    def __str__(self) -> str:
        return f"StudentSelection(student_id: {self.student_id}, company_id: {self.company_id}, block: {self.block})"

    def to_table_row(self):
        return [self.student_id, self.company_id, self.block, self.slot]

    @staticmethod
    def from_row(db_row):
        return StudentSelection(
            student_id=db_row["student_id"],
            company_id=db_row["company_id"],
            block=db_row["block"],
            slot=db_row["slot"],
        )


class Student(DatabaseModel):
    id: str
    name: str
    grade: str

    def __init__(self, name: str, grade: str, id="") -> None:
        self.name = name
        self.grade = grade
        self.id = id

    def __str__(self) -> str:
        return f"Schueler(id: {self.id}, name: {self.name}, grade: ${self.grade})"

    def to_table_row(self):
        return [self.name, self.grade]

    @staticmethod
    def from_row(db_row):
        return Student(id=db_row["id"], name=db_row["name"], grade=db_row["grade"])


class Company(DatabaseModel):
    id: str
    name: str
    capacity: int
    slots: dict[str, list[int]]

    def __init__(
        self,
        name: str,
        capacity: int,
        block1_slots: list[int],
        block2_slots: list[int],
        id="",
    ) -> None:
        self.name = name
        self.capacity = capacity
        self.id = id
        self.slots = {}
        self.slots["block1"] = block1_slots
        self.slots["block2"] = block2_slots

    def __str__(self) -> str:
        return f"Firma(id: {self.id}, name: {self.name}, slots: ${str(self.slots)}, capacity: ${self.capacity})"

    def to_table_row(self):
        return [self.name, self.capacity, self.slots["block1"], self.slots["block2"]]

    @staticmethod
    def from_row(db_row):
        return Company(
            id=db_row["id"],
            name=db_row["name"],
            capacity=db_row["capacity"],
            block1_slots=ast.literal_eval(db_row["block1_slots"]),
            block2_slots=ast.literal_eval(db_row["block2_slots"]),
        )
