import tkinter as tk


def center_window(self, width, height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


class Test(tk.Frame):
    def __init__(self, **args):
        super().__init__(**args)
        self.button = tk.Button(
            self, text="Close me", command=self.master.destroy
        ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    center_window(root, 300, 300)

    Test(master=root).pack()
    root.mainloop()
