# responsible for the GUI using tkinker
import os
import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import simpledialog
import pickle
from canvas import Canvas


def createButton(root, text, command):
    buttonWitdh = 70
    return tkinter.Button(root, text=text, width=buttonWitdh, command=command)


class UI:

    def __init__(self):
        # the main frame
        self.root = tkinter.Tk()
        self.root.title("MuralList")
        self.root.geometry("600x600")

        self.frame_tasks = tkinter.Frame(self.root)

        # tasks section
        self.listbox_tasks = tkinter.Listbox(
            self.frame_tasks, height=20, width=180)
        # self.listbox_tasks.grid(padx=20, pady=20)

        # scroll bar
        self.scrollbar_tasks = tkinter.Scrollbar(self.frame_tasks)
        self.listbox_tasks.config(yscrollcommand=self.scrollbar_tasks.set)
        self.scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # text input
        self.entry_task = tkinter.Entry(self.root, width=70)

        # button
        buttonWitdh = 70

        # st = Style()
        # st.configure('W.TButton', background='#345', foreground='black', font=('Arial', 14))

        self.button_add_task = createButton(
            self.root, "Add task", self.add_task)
        self.button_delete_task = createButton(
            self.root, "Delete task", self.delete_task)
        self.button_load_tasks = createButton(
            self.root, "Load tasks", self.load_tasks)
        self.button_save_tasks = createButton(
            self.root, "Save tasks", self.save_tasks)
        self.button_select = createButton(
            self.root, "Select an existing Background Image", self.select_img)
        self.button_generate = createButton(
            self.root, "Preview", self.generate_and_preview)
        self.button_make = createButton(
            self.root, "Customize Background Image", self.make)
        self.button_export = createButton(
            self.root, "Export Image", self.export)

        # image processing class canvas
        self.c = None
        self.background = None
        self.written_to_image = False

    def render(self):
        """
        basically create the frame and pack all the buttons generated in the constructor
        :return: nothing
        """
        self.frame_tasks.pack()
        self.scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.listbox_tasks.pack(side=tkinter.LEFT)
        self.entry_task.pack()
        self.button_add_task.pack()
        self.button_delete_task.pack()
        self.button_load_tasks.pack()
        self.button_save_tasks.pack()
        self.button_make.pack()
        self.button_select.pack()
        self.button_generate.pack()
        self.button_export.pack()
    # methods of the buttons

    def add_task(self):
        # get the input
        current_task = self.entry_task.get()
        if current_task:
            self.listbox_tasks.insert(tkinter.END, current_task)
            self.entry_task.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(
                title="Warning!", message="Can't enter an empty task! ")

    def delete_task(self):
        try:
            task_index = self.listbox_tasks.curselection()[0]
            self.listbox_tasks.delete(task_index)
            # if we deleted all the task from the task box, the image's task need to be deleted too
            self.c = self.background
            self.written_to_image = False
        except:
            tkinter.messagebox.showwarning(
                title="Warning!", message="You must select a task.")

    def load_tasks(self):
        try:
            tasks = pickle.load(open("../tasks.txt", "rb"))
            self.listbox_tasks.delete(0, tkinter.END)
            for task in tasks:
                self.listbox_tasks.insert(tkinter.END, task)
        except:
            tkinter.messagebox.showwarning(
                title="Warning!", message="Cannot find tasks.txt.")

    def save_tasks(self):
        tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
        pickle.dump(tasks, open("../tasks.txt", "wb"))

    def select_img(self):
        try:
            cwd = os.path.dirname(os.getcwd()) + "/pics"
            file_path = filedialog.askopenfilename(
                initialdir=cwd, title="Select a Picture")
            self.c = Canvas.open(file_path)
            self.background = self.c  # to keep a copy of the original file
            tkinter.messagebox.showinfo(message="Image opened successfully :D")
        except:
            tkinter.messagebox.showwarning(
                title="Warning", message="Image opened unsuccessfully")

    def generate_and_preview(self):
        try:
            if not self.written_to_image:
                tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
                for task in tasks:
                    self.c.addItemTo(task)
                self.c.addDate()
                self.written_to_image = True
            self.c.display()
        except:
            tkinter.messagebox.showwarning(
                title="Warning", message="You haven't loaded/created anything!")

    def make(self):
        try:
            width = simpledialog.askstring(
                title=" ", prompt="Please enter the width: ")
            height = simpledialog.askstring(
                title=" ", prompt="Please enter the height: ")
            (rgb, hx) = colorchooser.askcolor(
                title="Choose your background color")
            self.c = Canvas.make(int(width), int(height), hx)
            self.background = self.c  # to keep a copy of the original file
            tkinter.messagebox.showinfo(
                message="Image created successfully :D")
        except:
            tkinter.messagebox.showwarning(title="Warning", message="An error has occurred. Please check your input "
                                                                    "and try again")

    def export(self):
        if not self.written_to_image:
            tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
            for task in tasks:
                self.c.addItemTo(task)
            self.c.addDate()
            self.written_to_image = True
        cwd = os.path.dirname(os.getcwd()) + "/savedFiles"
        self.c.export(cwd)
        tkinter.messagebox.showinfo(message="Successfully saved to " + cwd)

    def run(self):
        """
        to start running the UI
        :return: nothing
        """
        self.root.mainloop()
