from random import random, seed
from datetime import datetime as dt

from application.people import People, get_employees
from application.salary import Salary


BASE_SALARY = 100_000

def main():
    seed(10)
    pair = [('Иван', 'Иванов'), ('Максим', 'Максимов'), ('Александр', 'Александров')]
    lst_ppls = [People(*elem) for elem in pair]
    print(f'Текущее время:\n{dt.now().strftime("%A, %d-%b-%Y %H:%M:%S")}')

    print(get_employees(lst_ppls))

    mounth_salary = Salary(BASE_SALARY)
    actual_salary = mounth_salary.calculate_salary(int(random() * 100))
    print(f'В этом месяце наш оклад равен {actual_salary}')

if __name__ == '__main__':
    main()
