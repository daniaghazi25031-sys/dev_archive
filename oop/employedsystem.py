# 1. تعريف الكلاس الأساسي (Encapsulation)
class Employee:
    def __init__(self, name, salary):
        self.name = name            # Public
        self.__salary = salary      # Private (Encapsulation)

    # Setter: لتعديل الراتب بأمان
    def set_salary(self, amount):
        if amount > 0:
            self.__salary = amount
        else:
            print("خطأ: الراتب لا يمكن أن يكون سالباً!")

    # Getter: للحصول على الراتب
    def get_salary(self):
        return self.__salary

    def work(self):
        print(f"{self.name} يؤدي مهامه العامة.")

# 2. الوراثة (Inheritance) و (Polymorphism)
class Developer(Employee):
    def __init__(self, name, salary, lang):
        # استدعاء مشيد الكلاس الأب
        super().__init__(name, salary)
        self.lang = lang

    # Override: تغيير سلوك الدالة للكلاس الابن
    def work(self):
        print(f"المبرمج {self.name} يكتب كود بلغة {self.lang}.")

class Manager(Employee):
    def work(self):
        print(f"المدير {self.name} يتابع سير المشروع.")

# --- تجربة الكود ---

# إنشاء كائنات
dev = Developer("علي", 5000, "Python")
mgr = Manager("سارة", 8000)

# استعراض تعدد الأشكال (Polymorphism)

f=[dev,mgr]
for emp in f :
    emp.work()  # كل كائن سيعمل بطريقته الخاصة رغم أننا ننادي نفس الدالة

# تجربة التغليف (Private members)
dev.set_salary(6000)
print(f"راتب المبرمج الجديد: {dev.get_salary()}")