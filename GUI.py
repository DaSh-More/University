import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mainloop()


def main():
    win = MainWindow()


if __name__ == "__main__":
    main()
