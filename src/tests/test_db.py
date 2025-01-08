import unittest
import random

from src.model.model import Model
from src.tests.test_generation import generate_test_data


class DBTest(unittest.TestCase):
    schueler_count = 160
    firm_count = 15
    klassen_grenze = 4
    class_count = 8

    def setUp(self) -> None:
        (
            self.schueler_wahlen,
            self.schueler_klassen,
            self.firmen_kapazitaet,
        ) = generate_test_data(
            schueler_count=self.schueler_count,
            firm_count=self.firm_count,
            class_count=self.class_count,
        )
        # Insert into database
        self.model = Model()
        self.model.clear_database()

    def test_insert_db(self):
        for key, value in self.schueler_klassen.items():
            firstname, lastname = key.split("_")
            self.model.create_student(firstname, lastname, value)

        for key, value in self.firmen_kapazitaet.items():
            self.model.create_company(
                f"Firma {key}",
                value,
                random.sample(range(1, 4), random.sample([1, 2, 3], 1)[0]),
                random.sample(range(1, 4), random.sample([1, 2, 3], 1)[0]),
            )
        for student, choice in self.schueler_wahlen.items():
            firstname, lastname = student.split("_")
            for block in ["block1", "block2"]:
                for index, company in enumerate(choice[block]):
                    self.model.create_selection(
                        name=f"{lastname}, {firstname}",
                        company_name=f"Firma {company}",
                        block=int(float(block.replace("block", ""))),
                        slot=index,
                    )
