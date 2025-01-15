import tkinter as tk
from tkinter import ttk
from src.view.tabs.company_tab import CompanyTab
from src.view.tabs.generate_tab import GenerateTab
from src.view.tabs.selection_tab import SelectionTab
from src.view.tabs.student_tab import StudentTab


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.title("Tabbed Application")
        self.geometry("800x600")

        # Tabs setup
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        CompanyTab(self.notebook, self.controller)
        student_tab = StudentTab(self.notebook, self.controller)
        selection_tab = SelectionTab(self.notebook, self.controller)
        GenerateTab(self.notebook, self.controller)

        def on_tab_change(*args):
            selected_tab = self.notebook.tab(self.notebook.select(), "text")
            if selected_tab == "Belegungen":
                selection_tab.update_view()
            elif selection_tab == "Schüler":
                student_tab.update_table_data()

        self.notebook.bind("<<NotebookTabChanged>>", on_tab_change)
