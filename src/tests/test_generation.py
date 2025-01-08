import random
import unittest
from collections import defaultdict

from ..plan_generation import generate_plan


def generate_test_data(schueler_count=50, firm_count=6, class_count=8):
    klassen = [str(i) for i in range(1, class_count + 1)]
    schueler_wahlen = {}
    schueler_klassen = {}
    klasse_besetzung = defaultdict(int)
    klasse_index = 0

    # Firmenkapazitäten zufällig festlegen (z.B. zwischen 10 und 30)
    firmen_kapazitaet = {i: random.randint(20, 30) for i in range(1, firm_count + 1)}

    for i in range(1, schueler_count + 1):
        schueler_name = f"Schueler_{i}"
        klasse_besetzung[klassen[klasse_index]] = (
            klasse_besetzung[klassen[klasse_index]] + 1
        )
        schueler_klassen[schueler_name] = klassen[klasse_index]
        if klasse_besetzung[klassen[klasse_index]] >= 20:
            klasse_index += 1

        # Firmenwahlen zufällig auswählen (jeweils 3 Firmen für Block 1 und Block 2)
        block1_wahl = random.sample(range(1, firm_count + 1), 3)
        block2_wahl = random.sample(range(1, firm_count + 1), 3)

        schueler_wahlen[schueler_name] = {
            "block1": block1_wahl,
            "block2": block2_wahl,
        }

    return schueler_wahlen, schueler_klassen, firmen_kapazitaet


class GeneratingTest(unittest.TestCase):
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

        self.result = generate_plan(
            schueler_wahlen=self.schueler_wahlen,
            firmen_kapazitaet=self.firmen_kapazitaet,
            klassen_grenze=self.klassen_grenze,
            slots_pro_block=3,
            schueler_klassen=self.schueler_klassen,
        )

    def test_result_length(self):
        self.assertEqual(len(self.result), self.schueler_count)

    def test_company_capacity(self):
        firmen_belegung = {}
        for student in self.result:
            for block in ["block1", "block2"]:
                for i in [1, 2, 3]:
                    key = f"{block}_{i}"
                    firmen_belegung.setdefault(student[key], {})
                    firmen_belegung[student[key]].setdefault(key, 0)
                    firmen_belegung[student[key]][key] += 1
        for key, value in firmen_belegung.items():
            max_capacity = self.firmen_kapazitaet[key]
            self.assertTrue(all(value <= max_capacity for value in value.values()))

    def test_max_class_attendence(self):
        for block in ["block1", "block2"]:
            for slot in [1, 2, 3]:
                slot_attendence = {}
                for student in self.result:
                    company = student[f"{block}_{slot}"]
                    klasse = self.schueler_klassen[student["name"]]
                    slot_attendence.setdefault(f"{block}_{slot}_{company}", {})
                    slot_attendence[f"{block}_{slot}_{company}"].setdefault(klasse, 0)
                    slot_attendence[f"{block}_{slot}_{company}"][f"{klasse}"] += 1
                for value in slot_attendence.values():
                    self.assertTrue(
                        all(value <= self.klassen_grenze for value in value.values())
                    )

    def test_student_max_attendence(self):
        for student in self.result:
            for block in ["block1", "block2"]:
                company_map = defaultdict(int)
                for slot in [1, 2, 3]:
                    company_map[student[f"{block}_{slot}"]] += 1
                self.assertTrue(all(value <= 1 for value in company_map.values()))
