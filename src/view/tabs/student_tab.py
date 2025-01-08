import tkinter as tk
from tkinter import ttk

from src.controller.controller import Controller
from src.util.functions import check_empty_fields
from src.view.generic_tree_view import GenericTreeView


class StudentTab(ttk.Frame):
    def __init__(self, root: ttk.Notebook, controller: Controller):
        super().__init__(root)
        self.controller = controller

        root.add(self, text="Schüler")
        input_container = ttk.Frame(self)

        tk.Label(input_container, text="Vorname:").grid(row=0, column=0, padx=5, pady=5)
        self.vorname_entry = tk.Entry(input_container)
        self.vorname_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_container, text="Nachname:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.nachname_entry = tk.Entry(input_container)
        self.nachname_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_container, text="Klasse:").grid(row=2, column=0, padx=5, pady=5)
        self.klasse = tk.Entry(input_container)
        self.klasse.grid(row=2, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(
            input_container,
            text="Eintragen",
            state="disabled",
            command=self.submit_student,
        )
        self.vorname_entry.bind("<KeyRelease>", self.validate_fields)
        self.nachname_entry.bind("<KeyRelease>", self.validate_fields)
        self.klasse.bind("<KeyRelease>", self.validate_fields)

        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)
        input_container.pack()

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        tree_container = tk.Frame(self, pady=10)

        self.generic_tree = GenericTreeView(
            tree_container,
            self.controller,
            ["Name", "Klasse"],
            self.make_table_list(),
            on_delete=self.controller.delete_student,
        )
        tree_container.pack()

    def make_table_list(self):
        students = self.controller.get_all_students()
        return list(
            map(
                lambda student: [student.name, student.grade],
                students,
            )
        )

    def update_table_data(self):
        self.generic_tree.update_data(self.make_table_list())

    def submit_student(self):
        self.controller.submit_schueler(
            vorname=self.vorname_entry.get(),
            nachname=self.nachname_entry.get(),
            klasse=self.klasse.get(),
        )
        self.update_table_data()

        self.vorname_entry.delete(0, tk.END)
        self.nachname_entry.delete(0, tk.END)
        self.klasse.delete(0, tk.END)

    def validate_fields(self, *args):
        check_empty_fields(
            self.vorname_entry,
            self.nachname_entry,
            self.klasse,
            button=self.submit_button,
        )
