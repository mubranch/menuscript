from tkinter import filedialog
import tkinter as tk


def main():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    print(file)
    root.destroy()


if __name__ == "__main__":
    main()
