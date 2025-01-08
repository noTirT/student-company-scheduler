from tkinter import filedialog


class DirectorySelector:
    def __init__(self):
        pass

    @staticmethod
    def show_dialog():
        dir = filedialog.askdirectory()
        return dir
