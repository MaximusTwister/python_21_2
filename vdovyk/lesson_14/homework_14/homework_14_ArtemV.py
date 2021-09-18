from abc import abstractmethod
from faker import Faker
import random


from project_constants import QUALIFICATION_LIST
from project_constants import SPECIALIZATION


fkr = Faker()


class Department:

    employees_list = []

    def __init__(self):
        self.department_info = self.get_department()

    @staticmethod
    def get_department_name():
        department_name = random.randint(1, 100)
        return department_name

    def get_department(self):
        department_info_list = dict.fromkeys(['department_name', 'number of workers', 'employees'])
        department_info_list['department_name'] = self.get_department_name()
        department_info_list['employees'] = self.employees_list
        department_info_list['number of workers'] = 0
        return department_info_list

    def hire_employee(self):
        if self.get_employee_info():
            hire_employee = self.get_employee_info()
            self.employees_list.append(hire_employee)
            self.department_info['number of workers'] += 1
            print(f'{hire_employee["name"]} got the position '
                  f'in the Department #{self.department_info["department_name"]}')

    def fire_employee(self):
        try:
            fire_employee = random.choice(self.employees_list)
            self.employees_list.remove(fire_employee)
            self.department_info['number of workers'] -= 1
            print(f'{fire_employee["name"]} lost the position '
                  f'in the Department #{self.department_info["department_name"]}')
        except IndexError:
            print(f'Department #{self.department_info["department_name"]} has not employees')

    @abstractmethod
    def get_employee_info(self):
        """ This method implements move functionality """
        pass


class Employee(Department):

    @classmethod
    def get_employee_info(cls):
        employee = dict()
        employee['name'] = fkr.name()
        employee['qualification'] = random.choice(QUALIFICATION_LIST)
        employee['specialization'] = random.choice(SPECIALIZATION)
        employee['work_experience_in_company'] = random.randint(0, 10)
        employee['salary'] = random.randint(500, 10000)
        return employee


emp = Employee()



