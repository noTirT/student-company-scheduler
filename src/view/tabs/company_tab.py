import tkinter as tk
from tkinter import ttk

from src.controller.controller import Controller
from src.util.functions import check_empty_fields
from src.view.generic_tree_view import GenericTreeView


class CompanyTab(ttk.Frame):
    def __init__(self, root: ttk.Notebook, controller: Controller):
        super().__init__(root)
        self.controller = controller.company_controller
        root.add(self, text="Firmen")
        input_container = ttk.Frame(self, padding=(0, 10))
        basic_container = ttk.Frame(input_container)
        tk.Label(basic_container, text="Firmenname:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.firmenname_entry = tk.Entry(basic_container)
        self.firmenname_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(basic_container, text="Kapazität:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.kapazitaet_entry = tk.Entry(basic_container, validate="key")
        self.kapazitaet_entry.grid(row=1, column=1, padx=5, pady=5)

        def validate_number_input(character):
            return character.isdigit()

        reg = self.register(validate_number_input)
        self.kapazitaet_entry.config(validatecommand=(reg, "%S"))

        submit_button = tk.Button(
            self,
            text="Eintragen",
            state="disabled",
            command=lambda: self.submit_company(),
        )

        self.firmenname_entry.bind(
            "<KeyRelease>",
            lambda _: check_empty_fields(
                self.firmenname_entry, self.kapazitaet_entry, button=submit_button
            ),
        )
        self.kapazitaet_entry.bind(
            "<KeyRelease>",
            lambda _: check_empty_fields(
                self.firmenname_entry, self.kapazitaet_entry, button=submit_button
            ),
        )
        basic_container.pack(side=tk.LEFT)

        vert_separator = ttk.Separator(input_container, orient="vertical")
        vert_separator.pack(fill="y", side=tk.LEFT)

        slot_container = ttk.Frame(input_container)
        tk.Label(slot_container, text="Block 1", relief="ridge").grid(
            row=0, column=1, padx=5, pady=5
        )
        tk.Label(slot_container, text="Block 2", relief="ridge").grid(
            row=0, column=2, padx=5, pady=5
        )

        self.checkbox_values = {"block1": [], "block2": []}

        for i, slot in enumerate(["Slot 1", "Slot 2", "Slot 3"], start=1):
            tk.Label(slot_container, text=slot).grid(
                row=0 + i, column=0, padx=5, pady=5, sticky="w"
            )

            # Checkboxes for Block 1 and Block 2
            block1_var = tk.BooleanVar()
            block2_var = tk.BooleanVar()

            self.checkbox_values["block1"].append(block1_var)
            self.checkbox_values["block2"].append(block2_var)

            tk.Checkbutton(slot_container, variable=block1_var).grid(
                row=0 + i, column=1, padx=5, pady=5
            )
            tk.Checkbutton(slot_container, variable=block2_var).grid(
                row=0 + i, column=2, padx=5, pady=5
            )

        slot_container.pack(side=tk.LEFT)
        input_container.pack()
        submit_button.pack()

        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x")

        database_container = tk.Frame(self, pady=10)
        self.generic_tree = GenericTreeView(
            database_container,
            self.controller,
            ["Firmenname", "Kapazität", "Block 1 Slots", "Block 2 Slots"],
            self.make_table_list(),
            on_delete=self.controller.delete_firmen,
        )
        database_container.pack()

    def make_table_list(self):
        companies = self.controller.get_all_firmen()
        table_companies = list(
            map(
                lambda company: [
                    company.name,
                    company.capacity,
                    company.slots["block1"],
                    company.slots["block2"],
                ],
                companies,
            )
        )
        return table_companies

    def submit_company(self):
        self.controller.submit_firmen(
            self.firmenname_entry.get(),
            self.kapazitaet_entry.get(),
            slot_selection=self.checkbox_values,
        )

        self.generic_tree.update_data(self.make_table_list())

        self.firmenname_entry.delete(0, tk.END)
        self.kapazitaet_entry.delete(0, tk.END)

        for val in [*self.checkbox_values["block1"], *self.checkbox_values["block2"]]:
            val.set(False)
