from src.model.model import Model
from src.model.models import Student


class StudentController:
    def __init__(self, model: Model):
        self.model = model

    def submit_schueler(self, vorname, nachname, klasse):
        # Add database logic here
        self.model.create_student(vorname, nachname, klasse)

    def get_all_students(self) -> list[Student]:
        return self.model.get_all_students()

    def delete_student(self, item):
        self.model.delete_student(item[0])

    def get_student_grades(self) -> dict[str, str]:
        all_students = self.model.get_students_with_selection()
        student_grades = {}
        for student in all_students:
            student_grades[student.name] = student.grade
        return student_grades

    def get_available_grades(self) -> list[str]:
        grades = self.model.get_available_grades()
        return list(set(grades))

    def get_student_choices(self):
        all_students = self.model.get_students_with_selection()
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

    def get_selection_student_options(self):
        students_without_selections = self.model.get_selection_student_options()

        options = []
        for index, student in enumerate(students_without_selections):
            if student.name in options:
                options.append(student.name + str(index))
            else:
                options.append(student.name)

        return options
