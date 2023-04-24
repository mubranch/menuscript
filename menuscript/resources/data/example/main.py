import tkinter as tk
import webbrowser
from functools import partial


def center_window(self, width, height):
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


class Test(tk.Frame):
    def __init__(self, **args):
        super().__init__(**args)
        self.configure(background="white", padx=10, pady=10)
        self.title = "Welcome!"

        tk.Label(
            self, bg="white", text="Welcome to MenuScript", font=("system", 16, "bold")
        ).pack(pady=12)

        tk.Label(
            self,
            text="Read the documentation before you get started.",
            font=("system", 12),
            bg="white",
            wraplength=250,
        ).pack(pady=10)

        self.button = tk.Button(
            self,
            text="Go to Docs",
            command=partial(
                webbrowser.open, "https://www.github.com/mubranch/menuscript"
            ),
            highlightbackground="white",
        ).pack(pady=12)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hello!")
    root.configure(bg="white")
    root.resizable(False, False)
    center_window(root, 300, 200)

    Test(master=root).pack()
    root.mainloop()
    root.destroy()
