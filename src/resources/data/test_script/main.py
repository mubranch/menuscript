import tkinter as tk

class Test(tk.Frame):
    def __init__(self, **args):
        super().__init__(**args)
        self.button = tk.Button(self, text="Close me", command=self.master.destroy).pack()
        
        
if __name__ == "__main__":
    root = tk.Tk()
    Test(master=root).pack()
    root.mainloop()