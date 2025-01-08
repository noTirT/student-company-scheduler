from src.model.db_handler import initialize_db
from src.model.model import Model
from src.controller.controller import Controller

from src.view.view import View


if __name__ == "__main__":
    initialize_db()

    model = Model()
    controller = Controller(model)
    view = View(controller)
    view.mainloop()
