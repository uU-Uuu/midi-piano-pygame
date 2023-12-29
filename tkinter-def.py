import tkinter
from tkinter import filedialog, messagebox



def open_file():
    top = tkinter.Tk()
    top.withdraw()
    file_name = filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def midifileErrorMessage():
    top = tkinter.Tk()
    top.withdraw()
    messagebox.showerror('Error reading the file', 'Please select a .mid file')
    top.destroy()
    return None
