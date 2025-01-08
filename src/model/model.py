from src.model.repos.company_repository import CompanyRepository
from src.model.db_handler import get_db_connection
from src.model.models import Company, Student, StudentSelection
from src.model.repos.student_repository import StudentRepository
from src.model.repos.student_selection_repository import StudentSelectionRepository


class Model:
    def __init__(self):
        self.db = get_db_connection()
        self.company_repo = CompanyRepository(self.db)
        self.student_repo = StudentRepository(self.db)
        self.student_selection_repo = StudentSelectionRepository(self.db)

    def clear_database(self):
        self.company_repo.delete_all()
        self.student_selection_repo.delete_all()
        self.student_repo.delete_all()

    def create_company(
        self, name: str, capacity: int, block1_slots: list[int], block2_slots: list[int]
    ):
        company = Company(
            name=name,
            capacity=capacity,
            block2_slots=block2_slots,
            block1_slots=block1_slots,
        )
        self.company_repo.create_company(company)

    def get_all_companies(self) -> list[Company]:
        return self.company_repo.get_all_companies()

    def create_student(self, first_name, last_name, grade):
        student = Student(f"{last_name}, {first_name}", grade)
        self.student_repo.create_student(student)

    def get_all_students(self) -> list[Student]:
        return self.student_repo.get_all_students()

    def delete_company(self, name: str):
        self.company_repo.delete(name)

    def create_selection(self, name, company_name, block, slot):
        student = self.student_repo.get_student_by_name(name)
        company = self.company_repo.get_company_by_name(company_name)

        self.student_selection_repo.create_student_selection(
            int(float(student.id)), int(float(company.id)), block, slot
        )

    def get_all_selections_ordered(self) -> list[StudentSelection]:
        return self.student_selection_repo.get_all_selections_ordered()

    def get_company_by_id(self, id: str) -> Company:
        return self.company_repo.get_company_by_id(id)

    def get_student_by_id(self, id: str) -> Student:
        return self.student_repo.get_student_by_id(id)

    def delete_student(self, name: str):
        self.student_repo.delete_student(name)

    def delete_selection(self, student_name: str):
        self.student_selection_repo.delete_selection_by_student_name(student_name)

    def get_student_by_name(self, name: str) -> Student:
        return self.student_repo.get_student_by_name(name)
