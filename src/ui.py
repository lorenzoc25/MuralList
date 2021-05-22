# responsible for the GUI using tkinker
import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import pickle
from canvas import Canvas


class UI:
    def __init__(self):
        # the main frame
        self.root = tkinter.Tk()
        self.root.title("ReM!ndMe")
        self.root.geometry("600x600")

        self.frame_tasks = tkinter.Frame(self.root)

        # tasks section
        self.listbox_tasks = tkinter.Listbox(
            self.frame_tasks, height=20, width=180)
        #self.listbox_tasks.grid(padx=20, pady=20)

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

        self.button_add_task = tkinter.Button(
            self.root, text="Add task", width=buttonWitdh, command=self.add_task)  # style='W.TButton'
        self.button_delete_task = tkinter.Button(
            self.root, text="Delete task", width=buttonWitdh, command=self.delete_task)
        self.button_load_tasks = tkinter.Button(
            self.root, text="Load tasks", width=buttonWitdh, command=self.load_tasks)
        self.button_save_tasks = tkinter.Button(
            self.root, text="Save tasks", width=buttonWitdh, command=self.save_tasks)
        self.button_select = tkinter.Button(
            self.root, text="Select Image", width=buttonWitdh, command=self.select_img_and_generate)

        # image processing class canvas

    def render(self):
        self.frame_tasks.pack()
        self.scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.listbox_tasks.pack(side=tkinter.LEFT)
        self.entry_task.pack()
        self.button_add_task.pack()
        self.button_delete_task.pack()
        self.button_load_tasks.pack()
        self.button_save_tasks.pack()
        self.button_select.pack()

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
        except:
            tkinter.messagebox.showwarning(
                title="Warning!", message="You must select a task.")

    def load_tasks(self):
        try:
            tasks = pickle.load(open("tasks.dat", "rb"))
            self.listbox_tasks.delete(0, tkinter.END)
            for task in tasks:
                self.listbox_tasks.insert(tkinter.END, task)
        except:
            tkinter.messagebox.showwarning(
                title="Warning!", message="Cannot find tasks.tsk.")

    def save_tasks(self):
        tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
        print(type(tasks))
        pickle.dump(tasks, open("tasks.tsk", "wb"))

    def get_task_as_strs(self):
        return self.listbox_tasks.get(0, self.listbox_tasks.size())

    def select_img_and_generate(self):
        file_path = filedialog.askopenfilename()
        c = Canvas.open(file_path)
        tasks = self.get_task_as_strs()
        for task in tasks:
            c.addItemTo(task)
        c.addDate()

    def run(self):
        self.root.mainloop()
