from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from database import Database
import datetime
from tkinter import ttk

class TodoApp:
    def __init__(self, root):
        self.db = Database('todo.db')
        self.root = root
        self.root.title("To-Do List Application")

        # Input Frame
        input_frame = Frame(self.root)
        input_frame.pack(pady=10)

        # Task Name
        self.task_name = StringVar()
        Label(input_frame, text="Task Name").grid(row=0, column=0, padx=10)
        Entry(input_frame, textvariable=self.task_name).grid(row=0, column=1, padx=10)

        # Task Priority
        self.task_priority = StringVar(value="Low")  # Default to Low
        Label(input_frame, text="Task Priority").grid(row=0, column=2, padx=10)
        OptionMenu(input_frame, self.task_priority, "Low", "Medium", "High").grid(row=0, column=3, padx=10)

        # Do By Date
        self.do_by_date = StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))  # Default to today's date
        Label(input_frame, text="Do By Date (YYYY-MM-DD)").grid(row=0, column=4, padx=10)
        Entry(input_frame, textvariable=self.do_by_date).grid(row=0, column=5, padx=10)

        # Date Selection Frame
        date_frame = Frame(self.root)
        date_frame.pack(pady=10)

        # Year ComboBox
        Label(date_frame, text="Year").grid(row=1, column=0, padx=5)
        self.year_var = StringVar()
        year_cb = ttk.Combobox(date_frame, textvariable=self.year_var, width=5, state="readonly")
        year_cb['values'] = [str(year) for year in range(2024, 2035)]
        year_cb.grid(row=2, column=0, padx=10)
        year_cb.bind('<<ComboboxSelected>>', self.update_date)

        # Month ComboBox
        Label(date_frame, text="Month").grid(row=1, column=1, padx=5)
        self.month_var = StringVar()
        month_cb = ttk.Combobox(date_frame, textvariable=self.month_var, width=3, state="readonly")
        month_cb['values'] = [f'{month:02}' for month in range(1, 13)]
        month_cb.grid(row=2, column=1, padx=10)
        month_cb.bind('<<ComboboxSelected>>', self.update_date)

        # Day ComboBox
        Label(date_frame, text="Day").grid(row=1, column=2, padx=5)
        self.day_var = StringVar()
        day_cb = ttk.Combobox(date_frame, textvariable=self.day_var, width=3, state="readonly")
        day_cb['values'] = [f'{day:02}' for day in range(1, 32)]
        day_cb.grid(row=2, column=2, padx=10)
        day_cb.bind('<<ComboboxSelected>>', self.update_date)

        # Set default values for ComboBoxes to today's date
        today = datetime.date.today()
        self.year_var.set(str(today.year))
        self.month_var.set(f'{today.month:02}')
        self.day_var.set(f'{today.day:02}')

        # Button Frame
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        # Buttons
        Button(button_frame, text="Add Task", command=self.add_task).pack(side=LEFT, padx=5)
        Button(button_frame, text="Remove Selected Task", command=self.remove_task).pack(side=LEFT, padx=5)
        Button(button_frame, text="Mark Task as Completed", command=self.complete_task).pack(side=LEFT, padx=5)

        self.tasks = Treeview(self.root, columns=("ID", "Name", "Priority", "Due Date", "Completed"), show="headings")
        self.tasks.pack()
        self.tasks.heading("ID", text="ID")
        self.tasks.heading("Name", text="Name")
        self.tasks.heading("Priority", text="Priority")
        self.tasks.heading("Due Date", text="Due Date")
        self.tasks.heading("Completed", text="Completed")

        self.populate_tasks()

    def update_date(self, event):
        # Update the 'Do By Date' entry with the selected year, month, and day
        pass

    def add_task(self):
        pass
        


    def populate_tasks(self):
        pass

    def remove_task(self):
        pass

    def complete_task(self):
        pass

if __name__ == "__main__":
    root = Tk()
    todo_app = TodoApp(root)
    root.mainloop()

