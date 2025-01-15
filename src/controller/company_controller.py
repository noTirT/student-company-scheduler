import tkinter as tk

from src.model.model import Model
from src.model.models import Company


class CompanyController:
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

    def get_all_firmen(self) -> list[Company]:
        return self.model.get_all_companies()

    def delete_firmen(self, item):
        self.model.delete_company(item[0])

    def get_company_capacities(self) -> dict[str, int]:
        companies = self.get_all_firmen()
        company_capacities = {}
        for company in companies:
            company_capacities[company.name] = company.capacity

        return company_capacities
