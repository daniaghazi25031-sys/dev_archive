class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return "welcome in patient in hospial"

class patient(person):
    def __init__(self, name, age, patient_id, illness):
        super().__init__(name, age)
        self.patient_id = patient_id
        self.illness = illness
    def __str__(self):
        return "welcome in patient in hospial"    
    def __str__(self):
        return f"patient: {self.name}  id: {self.patient_id}  illness: {self.illness}"
    
class doctor(person):
    def __init__(self, name, age, specialty):
        super().__init__(name, age)
        self.specialty = specialty
        
    def __str__(self):
        return f"doctor: {self.name}  specialty: {self.specialty}"
    

class appointment:
    def __init__(self, patientobj, doctorobj, date):
        self.patient = patientobj
        self.doctor = doctorobj
        self.date = date
    
        
    def __str__(self):
        return f"appointment: {self.patient.name} with {self.doctor.name} on {self.date}"

class hospital:
    def __init__(self, name):
        self.name = name
        self.patients = []
        self.doctors = []
        self.appointments = []
    

    def add_patient(self, p):
        self.patients.append(p)

    def add_doctor(self, d):
        self.doctors.append(d)

    def schedule(self, p, d, date):
        app = appointment(p, d, date)
        self.appointments.append(app)

    def disply_records(self):
        print(f"\n--- {self.name}  ---")
        
        print("\n patients")
        for p in self.patients:
            print(p)
            
        print("\n doctors")
        for d in self.doctors:
            print(d)
            
        print("\n appointments")
        for a in self.appointments: print(a)


my_hospital = hospital("city houspital")
    
p1 = patient("ema", 28, "p-998", "breack arm")
d1 = doctor("jassim", 39, "bount")
    
my_hospital.add_patient(p1)
my_hospital.add_doctor(d1)
my_hospital.schedule(p1, d1, "2026-05-07")
    
my_hospital.disply_records()