from tkinter import filedialog
import tkinter as tk


def main():
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()
    print(file)


if __name__ == "__main__":
    main()
