import tkinter as tk
from tkinter import ttk

settings = {
    'frame': {
        'borderwidth': '2px',
        'relief': tk.GROOVE,
    }
}


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.WinSettings()

    def WinSettings(self):
        self.title('Парсер вузов')
        self.geometry('600x400+200+100')
        self.left_column = tk.Frame(**settings['frame'])
        self.left_column.pack()
        self.right_column = tk.Frame(**settings['frame'])
        self.right_column.pack(side=tk.RIGHT)

        self.university_selector = ttk.Combobox(
            master=self.left_column, height=1)
        self.university_selector.pack()
        self.info = tk.Frame(master=self.left_column, **settings['frame'])
        self.info.pack()

        self.place = tk.Label(master=self.info, text='Место: 000')
        self.place.pack()
        self.original_place = tk.Label(
            master=self.info, text='Место среди оригиналов: 000')
        self.original_place.pack()

    def add_university(self, university):
        if isinstance(self.university_selector['values'], str):
            self.university_selector['values'] = (university,)
        else:
            self.university_selector['values'] += (university,)


def main():
    win = MainWindow()
    win.add_university('hello')
    win.add_university('hello1')
    win.mainloop()


if __name__ == "__main__":
    main()
