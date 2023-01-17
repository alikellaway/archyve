import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage


class App:
    def __init__(self, master):
        self.master = master
        master.title("Media Tools")

        self.sidebar = ttk.Frame(master, width=150)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        for i in range(3):
            self.sidebar.columnconfigure(i, weight=1)
            self.sidebar.rowconfigure(i, weight=1)

        # logo = PhotoImage(file="logo.png")  # change logo.png with your image path
        # self.logo_label = tk.Label(self.sidebar, image=logo)
        # self.logo_label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")
        self.button1 = ttk.Button(self.sidebar, text="Tab 1")
        self.button1.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

        self.button2 = ttk.Button(self.sidebar, text="Tab 2")
        self.button2.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

        self.button3 = ttk.Button(self.sidebar, text="Tab 3")
        self.button3.grid(row=3, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")


root = tk.Tk()
my_gui = App(root)
root.mainloop()
