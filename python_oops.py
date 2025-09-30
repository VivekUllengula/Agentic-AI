from abc import ABC, abstractmethod
import json

class AbstractEmployee(ABC): #Abstraction
    @abstractmethod
    def calculate_bonus(self):
        pass

class Employer(AbstractEmployee):

    def __init__(self, name, designation, salary):
        self.name = name
        self.designation = designation
        self.__salary = salary #Encapsulation

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self,value):
        if value < 0:
            raise ValueError("Salary cannot be Negative.")
        self.__salary = value

    def __str__(self):
        return f"The salary for the employee {self.name} with {self.designation} designation is {self.__salary}"

    def calculate_bonus(self): 
        return self.__salary * 0.15
    
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee: Employer):
        self.employees.append(employee)

    def total_salary(self):
        return sum(e.salary for e in self.employees)
        
    def total_bonus(self):
        return sum(e.calculate_bonus() for e in self.employees)

    def __str__(self):
        return f"Department: {self.name}, Employees: {len(self.employees)}"
    
    def find_by_name(self, name):
        return [e for e in self.employees if e.name.lower() == name.lower()]
    
    def high_earners(self, threshold):
        return [e for e in self.employees if e.salary > threshold]
    
class Manager(Employer):
    def __init__(self, name, designation, salary, team_size):
        super().__init__(name, designation, salary)
        self.team_size = team_size

    def __str__(self):
        return super().__str__() + f", Team Size: {self.team_size}"

class Intern(Employer):
    def calculate_bonus(self):
        return 0  # interns don’t get bonus
    
class EmployeeStore:
    def __init__(self, filename="employees.json"):
        self.filename = filename

    def save(self, employees):
        data = [self._serialize(e) for e in employees]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [self._deserialize(e) for e in data]
        except FileNotFoundError:
            return []
        
    def _serialize(self, employee):
        data = vars(employee).copy()
        if isinstance(employee, Manager):
            data['type'] = 'Manager'
        elif isinstance(employee, Intern):
            data['type'] = 'Intern'
        else:
            data['type'] = 'Employer'
        return data

    def _deserialize(self, data):
        emp_type = data.pop('type', 'Employer')
        if emp_type == 'Manager':
            return Manager(**data)
        elif emp_type == 'Intern':
            return Intern(**data)
        else:
            return Employer(**data)

# ===== Interactive CLI =====

def main():
    dept = Department("Engineering")
    store = EmployeeStore()
    dept.employees = store.load()

    while True:
        print("\n--- Employee Management ---")
        print("1. Add Employee")
        print("2. List Employees")
        print("3. Total Salary")
        print("4. Total Bonus")
        print("5. Find Employee by Name")
        print("6. High Earners")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            name = input("Name: ")
            designation = input("Designation: ")
            salary = float(input("Salary: "))
            emp_type = input("Type (Employer/Manager/Intern): ").strip().lower()
            
            if emp_type == "manager":
                team_size = int(input("Team Size: "))
                emp = Manager(name, designation, salary, team_size)
            elif emp_type == "intern":
                emp = Intern(name, designation, salary)
            else:
                emp = Employer(name, designation, salary)
            
            dept.add_employee(emp)
            store.save(dept.employees)
            print(f"Added: {emp}")

        elif choice == "2":
            if not dept.employees:
                print("No employees found.")
            for e in dept.employees:
                print(e)

        elif choice == "3":
            print("Total Salary:", dept.total_salary())

        elif choice == "4":
            print("Total Bonus:", dept.total_bonus())

        elif choice == "5":
            name = input("Enter name to search: ")
            found = dept.find_by_name(name)
            if found:
                for e in found:
                    print(e)
            else:
                print("No employee found.")

        elif choice == "6":
            threshold = float(input("Enter salary threshold: "))
            high = dept.high_earners(threshold)
            if high:
                for e in high:
                    print(e)
            else:
                print("No employees above threshold.")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()