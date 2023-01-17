import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Media Tools")
        self.geometry(f'{500}x{500}')

        df_button = tk.Button(text="Find Duplicates", command=self.to_duplicate_finder)
        df_button.pack()

    def to_duplicate_finder(self):
        self.clear()
        self.build_duplicate_finder()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def build_duplicate_finder(self):
        frame = tk.Frame()
        


if __name__ == '__main__':
    app = App()
    app.mainloop()
