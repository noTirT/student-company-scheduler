from src.controller.company_controller import CompanyController
from src.controller.selection_controller import SelectionController
from src.controller.student_controller import StudentController
from src.model.model import Model


class Controller:
    def __init__(self, model: Model):
        self.model = model
        self.selection_controller = SelectionController(model)
        self.company_controller = CompanyController(model)
        self.student_controller = StudentController(model)
