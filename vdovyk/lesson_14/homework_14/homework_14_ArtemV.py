from faker import Faker
import random


from constants import QUALIFICATION_LIST
from constants import SPECIALIZATION


fkr = Faker()


class Department:

    __employees_list = list()

    @classmethod
    def get_department_info(cls):
        return {'department_name': 'Awesome IT Company Department',
                'employees': [str(emp) for emp in cls.__employees_list],
                'workers_amount': len(cls.__employees_list)}

    @classmethod
    def add_department_worker(cls, worker):
        cls.__employees_list.append(worker)
        return f'{worker} got the position in {cls.get_department_info()["department_name"]}'

    @classmethod
    def remove_department_worker(cls, worker):
        if worker not in cls.__employees_list:
            return {'status_code': 404, 'msg': 'Not Found in DB'}
        cls.__employees_list.remove(worker)
        return f'{worker} lost the position in {cls.get_department_info()["department_name"]}'


class Employee(Department):

    def __init__(self):
        self.__employee = dict()
        self.__create_employee()

    def __str__(self):
        return self.__employee.get('name')

    def __create_employee(self):
        self.__employee['name'] = fkr.name()
        self.__employee['qualification'] = random.choice(QUALIFICATION_LIST)
        self.__employee['specialization'] = random.choice(SPECIALIZATION)
        self.__employee['work_experience_in_company'] = random.randint(0, 10)
        self.__employee['salary'] = random.randint(500, 10000)

    def get_employee_info(self):
        return self.__employee

    def hire_employee(self):
        res = self.add_department_worker(self)
        print(f'Hire Result: {res}')

    def fire_employee(self):
        res = self.remove_department_worker(self)
        print(f'Fire Result: {res}')


e = Employee()
