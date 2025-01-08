import tkinter as tk
from tkinter import ttk

from src.controller.controller import Controller
from src.util.functions import check_empty_fields
from src.view.generic_tree_view import GenericTreeView
from ttkwidgets.autocomplete import AutocompleteCombobox


class SelectionTab(ttk.Frame):
    def __init__(self, root: ttk.Notebook, controller: Controller):
        super().__init__(root)
        self.controller = controller

        root.add(self, text="Belegungen")
        container = ttk.Frame(self)

        tk.Label(container, text="Schüler").grid(row=0, column=0, padx=5, pady=5)
        students = self.controller.get_all_students()
        options = []
        for index, student in enumerate(students):
            if student.name in options:
                options.append(student.name + str(index))
            else:
                options.append(student.name)

        self.autocomplete_dropdown = AutocompleteCombobox(
            container, completevalues=options, postcommand=self.update_data
        )  # Replace dynamically
        self.autocomplete_dropdown.grid(row=0, column=1, padx=5, pady=5)

        grid_frame = ttk.Frame(container)
        grid_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Grid headers
        tk.Label(grid_frame, text="Block 1", relief="ridge").grid(
            row=0, column=1, padx=5, pady=5
        )
        tk.Label(grid_frame, text="Block 2", relief="ridge").grid(
            row=0, column=2, padx=5, pady=5
        )

        companies = self.controller.get_all_firmen()
        # Grid rows
        self.belegungen = {}
        for i, slot in enumerate(["Slot 1", "Slot 2", "Slot 3"], start=1):
            tk.Label(grid_frame, text=slot).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            block1_options = [
                company.name for company in companies if (i) in company.slots["block1"]
            ]
            block2_options = [
                company.name for company in companies if (i) in company.slots["block2"]
            ]

            self.belegungen[f"block1_slot{i}"] = AutocompleteCombobox(
                grid_frame, completevalues=block1_options
            )
            self.belegungen[f"block1_slot{i}"].grid(row=i, column=1, padx=5, pady=5)
            self.belegungen[f"block2_slot{i}"] = AutocompleteCombobox(
                grid_frame, completevalues=block2_options
            )
            self.belegungen[f"block2_slot{i}"].grid(row=i, column=2, padx=5, pady=5)

        for box in [*self.belegungen.values(), self.autocomplete_dropdown]:
            for sequence in [
                "<Return>",
                "<<ComboboxSelected>>",
                "<FocusOut>",
                "<KeyRelease>",
            ]:
                box.bind(sequence, self.validate_fields)

        self.submit_button = tk.Button(
            container,
            text="Eintragen",
            state="disabled",
            command=self.submit_selection,
        )
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        container.pack()
        tree_container = tk.Frame(self, padx=20)

        self.generic_tree = GenericTreeView(
            tree_container,
            self.controller,
            [
                "Schülername",
                "Block 1 Slot 1",
                "Block 1 Slot 2",
                "Block 1 Slot 3",
                "Block 2 Slot 1",
                "Block 2 Slot 2",
                "Block 2 Slot 3",
            ],
            self.make_table_list(),
            self.controller.delete_selection,
            horizontal_scrollbar=True,
        )

        tree_container.pack()

    def make_table_list(self):
        selections = self.controller.get_all_selections()
        result = []
        for key, value in selections.items():
            result.append([key, *value])

        return result

    def submit_selection(self):
        self.controller.submit_belegungen(
            student=self.autocomplete_dropdown.get(),
            belegungen={key: widget.get() for key, widget in self.belegungen.items()},
        )

        for box in [*self.belegungen.values(), self.autocomplete_dropdown]:
            box.delete(0, tk.END)

    def validate_fields(self, *args):
        check_empty_fields(
            self.autocomplete_dropdown,
            *self.belegungen.values(),
            button=self.submit_button,
        )

    def update_table_data(self):
        self.generic_tree.update_data(self.make_table_list())

    def update_data(self):
        students = self.controller.get_all_students()

        options = []
        for index, student in enumerate(students):
            if student.name in options:
                options.append(student.name + str(index))
            else:
                options.append(student.name)

        self.autocomplete_dropdown["values"] = options
