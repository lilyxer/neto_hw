from my_modules.my_classes import *
from random import randint, choice, seed


# наполняем данными
def students_eval(stud: Student, lect: Lecturer):
    """
    функция рандомно проставялет оценки лекторам от студентов.
    курсы должны совпадать
    результат выводится на печать и валидные оценки попадают в поле экземпляра
    """
    print(f'общие курсы у {stud.name} и {lect.name}: ', end='')
    print(*set(stud.courses_in_progress)&set(lect.courses_attached), sep=', ')
    for _ in range(20):
        stud.rate_lecturer(lecturer=lect, course=choice(all_courses),
                            grade=randint(1, 10))
    print(f'проверим правильность заполнения\n'
            f'Оценки лектора {lect.surname}\n'
            f'{lect.grades}\n'
            f'{"-"*80}')

def reviewer_eval(rev: Reviewer, stud: Student):
    """
    функция рандомно проставялет оценки студентам от экспертов.
    экспрет может оценивать все курсы 
    результат выводится на печать и валидные оценки попадают в поле экземпляра
    """
    print(f'общие курсы у {stud.name} и {rev.name}: ', end='')
    print(*set(rev.courses_attached)&set(stud.courses_in_progress), sep=', ')
    for _ in range(20):
        rev.rate_hw(student=stud, course=choice(all_courses), 
                    grade=randint(1, 10))
    print(f'проверим правильность заполнения\n'
            f'Оценки студента {stud.surname}\n'
            f'{stud.grades}\n'
            f'{"-"*80}')

def negative_check():
    """
    тесты на проверку
    """
    assert (student_1.rate_lecturer(lecturer=lecturer_1, 
                                    course='Python', grade=1) 
                                    == 'Python не является общим')
    
    assert ((student_1.rate_lecturer(lecturer=lecturer_1, 
                                        course='GO', grade=20)) 
                                        == '20 не является валидной оценкой')
    
    assert ((student_1.rate_lecturer(lecturer=lecturer_1, 
                                        course='GO', grade='2')) 
                                        == '2 не является валидной оценкой')
    
    assert ((student_1.rate_lecturer(lecturer=reviewer_1, 
                                        course='GO', grade=2)) 
                                        == 'Reviewerova не явлется лектором')
    
    assert ((reviewer_1.rate_hw(student=student_1, 
                                course='GO', grade='1')) 
                                == '1 не является валидной оценкой')
    
    assert (reviewer_1.rate_hw(student=student_1, 
                                course='Python', grade='1') 
                                == 'Python не является общим')

    assert (reviewer_1.rate_hw(student=lecturer_1, 
                                course='SQL', grade=1)
                                == 'Lectorova не явлется студентом')

def avg(lst: list) -> float:
    """
    lst - список с оценками
    return среднее арифмитическое
    """
    return round(sum(lst)/len(lst), 2)

def average_rating_course(peoples: list, course: str) -> float:
    """
    peoples - список студентов либо лекторов
    course - название курса
    у студента все оценки хранятся в поле grades
    """
    list_grades = []
    for people in peoples:
        if tmp := people.grades.get(course):
            list_grades.append(avg(tmp))
    return avg(list_grades) if list_grades else 0.0

if __name__ == '__main__':
    seed(100) # данные будут постоянны

    # создаем по 2 экземпляра: студента, лектора, эксперта
    student_1 = Student(name='Alexandra', surname='Studentova', gender='Female')
    student_2 = Student(name='Alexandr', surname='Studentov', gender='Male')
    lecturer_1 = Lecturer(name='Valeriya', surname='Lectorova')
    lecturer_2 = Lecturer(name='Valeriy', surname='Lectorov')
    reviewer_1 = Reviewer(name='Evgeniya', surname='Reviewerova')
    reviewer_2 = Reviewer(name='Evgeniy', surname='Reviewerov')

    # заполняем поля созданных экземпляров
    all_courses = ['GO', 'SQL', 'Git', 'JavaSript', 'Python']
    student_1.finished_courses.extend(['Git', 'CSS', 'HTML'])
    student_2.finished_courses.extend(['Основы программирования'])

    student_1.courses_in_progress.extend(['GO', 'SQL', 'JavaScript'])
    student_2.courses_in_progress.extend(['Python', 'Git', 'SQL'])

    lecturer_1.courses_attached.extend(['GO', 'SQL'])
    lecturer_2.courses_attached.extend(['Python', 'Git', 'JavaSript'])

    reviewer_1.courses_attached.extend(all_courses)
    reviewer_2.courses_attached.extend(all_courses)

    # ставим оценки преподавателям
    students_eval(stud=student_1, lect=lecturer_1)
    students_eval(stud=student_1, lect=lecturer_2)
    students_eval(stud=student_2, lect=lecturer_1)
    students_eval(stud=student_2, lect=lecturer_2)

    # ставим оценки студентам
    reviewer_eval(stud=student_1, rev=reviewer_1)
    reviewer_eval(stud=student_1, rev=reviewer_2)
    reviewer_eval(stud=student_2, rev=reviewer_1)
    reviewer_eval(stud=student_2, rev=reviewer_2)

    # тесты на негативные проверки
    negative_check()

    # средняя оценка по домашнему заданию за курс, у всех студентов
    print(average_rating_course(peoples=[student_1, student_2], course='Git'))
    print(average_rating_course(peoples=[student_1, student_2], course='SQL'))
    print(average_rating_course(peoples=[student_1, student_2], course='Python'))
    # средняя оценка по домашнему заданию за курс, у всех лекторов
    print(average_rating_course(peoples=[lecturer_1, lecturer_2], course='Git'))
    print(average_rating_course(peoples=[lecturer_1, lecturer_2], course='SQL'))
    print(average_rating_course(peoples=[lecturer_1, lecturer_2], course='Python'))
    
    