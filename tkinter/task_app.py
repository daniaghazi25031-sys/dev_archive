import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily To-Do List")
        self.root.geometry("400x450")

        self.label = tk.Label(root, text="Enter new task:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.task_entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.task_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#0E71EA", fg="white")
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Selected Task", command=self.delete_task, bg="#f44336", fg="white")
        self.delete_button.pack(pady=5)

        self.tasks_listbox = tk.Listbox(root, width=100, height=10, font=("Arial", 12))
        self.tasks_listbox.pack(pady=10, padx=10)

    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task first!")

    def delete_task(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()