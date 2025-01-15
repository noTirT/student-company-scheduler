from src.model.model import Model
from collections import defaultdict


class SelectionController:
    def __init__(self, model: Model):
        self.model = model

    def delete_selection(self, item):
        self.model.delete_selection(item[0])

    def get_all_selections(self) -> dict[str, list[str]]:
        selections_by_students = defaultdict(list[str])
        all_selections = self.model.get_all_selections_ordered()

        for selection in all_selections:
            company = self.model.get_company_by_id(str(selection.company_id))
            student = self.model.get_student_by_id(str(selection.student_id))
            selections_by_students[student.name].append(company.name)

        return selections_by_students

    def submit_belegungen(self, belegungen: dict[str, str], student: str):
        # Add database logic here
        for key, value in belegungen.items():
            block, slot = key.replace("block", "").replace("slot", "").split("_")
            self.model.create_selection(student, value, block, slot)
