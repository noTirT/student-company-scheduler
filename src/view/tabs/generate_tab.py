import tkinter as tk
from tkinter import ttk
import os
import time

from src.controller.controller import Controller
from src.csv_writer import CSVWriter
from src.plan_generation import generate_plan
from src.view.directory_selector import DirectorySelector
from src.view.generic_tree_view import GenericTreeView


class GenerateTab(ttk.Frame):
    def __init__(self, root: ttk.Notebook, controller: Controller):
        super().__init__(root)
        self.controller = controller
        self.plan = []
        root.add(self, text="Generieren")

        input_container = ttk.Frame(self)

        tk.Label(
            input_container, text="Maximale Schüler gleicher Klasse in Slot:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.limit_entry = tk.Entry(input_container, validate="key")
        self.limit_entry.insert(0, "4")
        self.limit_entry.grid(row=0, column=1, padx=5, pady=5)

        def validate_number_input(character):
            return character.isdigit()

        reg = self.register(validate_number_input)
        self.limit_entry.config(validatecommand=(reg, "%S"))

        self.generate_button = tk.Button(
            input_container, text="Plan generieren", command=self.generate_plan
        )
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        self.loading_var = tk.StringVar()
        self.loading_var.set("")
        self.loading_label = tk.Label(input_container, textvariable=self.loading_var)
        self.loading_label.grid(row=0, column=3, padx=5, pady=5)

        input_container.pack()

        seperator = ttk.Separator(self, orient="horizontal")
        seperator.pack(fill="x", pady=10)

        tree_container = tk.Frame(self)

        self.generic_tree = GenericTreeView(
            tree_container,
            self.controller,
            ["Name", "Klasse", "1-1", "1-2", "1-3", "2-1", "2-2", "2-3"],
            self.make_table_list(),
            horizontal_scrollbar=True,
        )
        tree_container.pack()

        download_container = ttk.Frame(self, padding=(10, 10))

        self.download_button = tk.Button(
            download_container,
            text="Exportieren zu CSV",
            command=self.print_to_csv,
            state="disabled",
        )

        self.download_button.pack()
        download_container.pack()

    def make_table_list(self) -> list[list[str]]:
        if not self.plan:
            return []
        return list(
            map(
                lambda plan_entry: [
                    plan_entry["name"],
                    plan_entry["klasse"],
                    plan_entry["block1_1"],
                    plan_entry["block1_2"],
                    plan_entry["block1_3"],
                    plan_entry["block2_1"],
                    plan_entry["block2_2"],
                    plan_entry["block2_3"],
                ],
                self.plan,
            )
        )

    def print_to_csv(self):
        directory = DirectorySelector.show_dialog()
        if self.plan:
            CSVWriter.to_csv(os.path.join(directory, "plan.csv"), self.plan)

    def generate_plan(self):
        self.loading_var.set("Loading...")
        self.update_idletasks()
        class_limit = int(float(self.limit_entry.get()))
        company_capacities = self.controller.get_company_capacities()
        student_grades = self.controller.get_student_grades()
        student_choices = self.controller.get_student_choices()

        self.plan = generate_plan(
            schueler_wahlen=student_choices,
            firmen_kapazitaet=company_capacities,
            klassen_grenze=class_limit,
            slots_pro_block=3,
            schueler_klassen=student_grades,
        )

        self.generic_tree.update_data(self.make_table_list())

        if len(self.plan) > 0:
            self.download_button["state"] = "normal"

        self.loading_var.set("")
