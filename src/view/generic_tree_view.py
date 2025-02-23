import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.controller.controller import Controller


class GenericTreeView(ttk.Treeview):
    def __init__(
        self,
        root: tk.Frame,
        controller: Controller,
        columns: list[str],
        data: list[list[str]],
        on_delete: Optional[Callable] = None,
        vertical_scrollbar: bool = True,
        horizontal_scrollbar: bool = False,
    ):
        self.controller = controller
        self.on_delete = on_delete

        self.root = root

        container = ttk.Frame(root)

        super().__init__(container, columns=columns, show="headings")

        for key in columns:
            self.heading(key, text=key)

        for entry in data:
            self.insert("", tk.END, values=entry)

        if vertical_scrollbar:
            self.add_vertical_scrollbar(container)

        if horizontal_scrollbar:
            self.add_horizontal_scrollbar(container)

        self.grid(row=0, column=0, sticky="nsew")

        if self.on_delete:
            self.bind("<Button-3>", self.show_context_menu)
            self.menu = tk.Menu(container, tearoff=0)
            self.menu.add_command(label="Löschen", command=self.delete_selected_item)

        container.pack(fill=tk.BOTH, expand=True)

    def add_vertical_scrollbar(self, container: ttk.Frame):
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.configure(yscrollcommand=scrollbar.set)

    def add_horizontal_scrollbar(self, container: ttk.Frame):
        scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.xview)
        scrollbar.grid(row=1, column=0, sticky="ew")
        self.configure(xscrollcommand=scrollbar.set)

    def show_context_menu(self, event):
        selected_item = self.identify_row(event.y)
        if selected_item:
            self.selection_set(selected_item)
            self.menu.tk_popup(event.x_root, event.y_root)

    def delete_selected_item(self):
        selected_item = self.selection()[0]
        item_values = self.item(selected_item, "values")
        if self.on_delete:
            self.on_delete(item_values)
        self.delete(selected_item)

    def update_data(self, data):
        for i in self.get_children():
            self.delete(i)

        for entry in data:
            self.insert("", tk.END, values=entry)
