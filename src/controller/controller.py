from src.model.model import Model
from src.model.models import Company, Student
import tkinter as tk
from collections import defaultdict

from src.plan_generation import generate_plan


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def submit_firmen(
        self,
        firmenname: str,
        kapazitaet: str,
        slot_selection: dict[str, list[tk.BooleanVar]],
    ):
        block1_slots = []
        block2_slots = []

        choices = slot_selection["block1"]
        for index, choice in enumerate(choices):
            if choice.get():
                block1_slots.append(index + 1)
        choices = slot_selection["block2"]
        for index, choice in enumerate(choices):
            if choice.get():
                block2_slots.append(index + 1)

        # Add database logic here
        self.model.create_company(
            firmenname,
            int(float(kapazitaet)),
            block1_slots=block1_slots,
            block2_slots=block2_slots,
        )

    def submit_klassen(self, klasse):
        print(f"Klasse: {klasse}")
        # Add database logic here

    def submit_schueler(self, vorname, nachname, klasse):
        # Add database logic here
        self.model.create_student(vorname, nachname, klasse)

    def submit_belegungen(self, belegungen: dict[str, str], student: str):
        # Add database logic here
        for key, value in belegungen.items():
            block, slot = key.replace("block", "").replace("slot", "").split("_")
            self.model.create_selection(student, value, block, slot)

    def get_all_firmen(self) -> list[Company]:
        return self.model.get_all_companies()

    def get_all_students(self) -> list[Student]:
        return self.model.get_all_students()

    def delete_firmen(self, item):
        self.model.delete_company(item[0])

    def get_all_selections(self) -> dict[str, list[str]]:
        selections_by_students = defaultdict(list[str])
        all_selections = self.model.get_all_selections_ordered()

        for selection in all_selections:
            company = self.model.get_company_by_id(str(selection.company_id))
            student = self.model.get_student_by_id(str(selection.student_id))
            selections_by_students[student.name].append(company.name)

        return selections_by_students

    def delete_student(self, item):
        self.model.delete_student(item[0])

    def delete_selection(self, item):
        self.model.delete_selection(item[0])

    def get_company_capacities(self) -> dict[str, int]:
        companies = self.get_all_firmen()
        company_capacities = {}
        for company in companies:
            company_capacities[company.name] = company.capacity

        return company_capacities

    def get_student_grades(self) -> dict[str, str]:
        all_students = self.get_all_students()
        student_grades = {}
        for student in all_students:
            student_grades[student.name] = student.grade
        return student_grades

    def get_student_choices(self):
        all_students = self.get_all_students()
        all_choices = self.model.get_all_selections_ordered()

        choices = {}
        for student in all_students:
            stud_choices = [c for c in all_choices if c.student_id == student.id]
            choices[student.name] = {
                "block1": [
                    self.model.get_company_by_id(str(c.company_id)).name
                    for c in stud_choices
                    if c.block == 1
                ],
                "block2": [
                    self.model.get_company_by_id(str(c.company_id)).name
                    for c in stud_choices
                    if c.block == 2
                ],
            }
        return choices
