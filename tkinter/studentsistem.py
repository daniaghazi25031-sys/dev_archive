import tkinter as tk
from tkinter import ttk, messagebox

class student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

class student_app:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("student system manage")
        # توحيد اسم القائمة
        self.students_list = []
        self.create_widgets()

    def create_widgets(self):
       
        input_frame = tk.LabelFrame(self.root, text="student registration", pady=10, padx=10)
        input_frame.pack(pady=20, fill="x", padx=20)
        
        tk.Label(input_frame, text="id:").grid(row=0, column=0, sticky="w")
        self.id_entry = tk.Entry(input_frame)
        self.id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="name:").grid(row=0, column=2, sticky="w")
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=3, pady=5, padx=5)

        tk.Label(input_frame, text="age:").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(input_frame)
        self.age_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="grade:").grid(row=1, column=2, sticky="w")
        self.grade_entry = tk.Entry(input_frame)
        self.grade_entry.grid(row=1, column=3, pady=5, padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=10)
        
        tk.Button(btn_frame, text="add student", command=self.add_student).pack(side="left", padx=10)
        tk.Button(btn_frame, text="clear", command=self.clear_fields).pack(side="left", padx=10)

        self.tree = ttk.Treeview(self.root, columns=("id", "name", "age", "grade"), show="headings")
        self.tree.heading("id", text="id")
        self.tree.heading("name", text="name")
        self.tree.heading("age", text="age")
        self.tree.heading("grade", text="grade")
        self.tree.column("id", width=50)
        self.tree.column("age", width=50)
        self.tree.pack(pady=20, fill="both", expand=True, padx=20)

    def add_student(self):
        s_id = self.id_entry.get()
        s_name = self.name_entry.get()
        s_age = self.age_entry.get()
        s_grade = self.grade_entry.get()
        
        if s_id and s_name and s_age and s_grade:
            new_student = student(s_id, s_name, s_age, s_grade)
            self.students_list.append(new_student)
            
            self.tree.insert("", "end", values=(
                new_student.student_id, 
                new_student.name, 
                new_student.age, 
                new_student.grade
            ))
            self.clear_fields()
        else:
            messagebox.showwarning("error", "fill all fields")

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = student_app(window)
    window.mainloop()