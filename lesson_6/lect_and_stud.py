from functools import total_ordering
from random import randint, choice, seed


class CourseError(BaseException):
    ...


class GradeError(BaseException):
    ...


class Mentor:
    def __init__(self, name: str, surname: str) -> None:
        """
        name: str - имя преподавателя 
        surname: str - фамилия преподавателя
        courses_attached - за каким курсовм закреплен
        """
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(\'{self.name}\', \'{self.surname}\')'


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name: str, surname: str) -> None:
        """
        grades_from_stud: dict - словарь с оценками от студентов по общему курсу {'python': []}
        """
        super().__init__(name, surname)
        self.grades_from_stud = {}

    def _get_all_grades(self) -> float|None:
        """
        метод лектора, собирает все оценки по всем предметам 
        в один массив и возвращает среднее если есть хотя бы одна оценка
        """
        all_grades = []
        if self.grades_from_stud:
            for x in self.grades_from_stud.values():
                all_grades.extend(x)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self) -> str:
        mean = self._get_all_grades()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {mean}'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() == other._get_all_grades()
        raise NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() < other._get_all_grades()
        raise NotImplemented


@total_ordering 
class Student:
    def __init__(self, name: str, surname: str, gender: str) -> None:
        """
        name: str - имя студента 
        surname: str - фамилия студента
        gender: str - пол студента
        finished_courses: list - завершенные курсы ['python', 'git', 'js']
        courses_in_progress: list - в процессе прохождения ['sql', 'html']
        grades: dict - отражает в себе все курсы, и оценки к ним в списке {'python': [], 'js': []}
        """
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer: Lecturer, course: str, grade: int) -> None:
        """
        метод студента, выставляет оценку лектору по общему курсу
        lecturer - должен быть class Lecturer
        course - название курса, курс должен быть как у лектора так и у студента
        grade - оценка должна быть в диапазоне 1-10
        """
        if isinstance(lecturer, Lecturer):
            if all(map(lambda x: course in x, (self.courses_in_progress, 
                                               lecturer.courses_attached))):
                if isinstance(grade, int) and grade in range(1, 11):
                    lecturer.grades_from_stud.setdefault(course, []).append(grade)
                    return True
                raise GradeError(f'{grade} не является валидной оценкой')
            raise CourseError(f'{course} не является общим')
        raise TypeError(f'{lecturer.surname} не явлется лектором')


    def _get_all_grades(self) -> float|None:
        """
        метод студента, собирает все оценки по всем предметам в обоих словарях
        в один массив и возвращает среднее если есть хотя бы одна оценка
        """
        all_grades = []
        if self.grades:
            for grade in self.grades.values():
                all_grades.extend(grade)

        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0
        
    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(\'{self.name}\','
                f' \'{self.surname}\', \'{self.gender}\')')

    def __str__(self) -> str:
        mean = self._get_all_grades()
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка  домашние задания: {mean}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __eq__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() == other._get_all_grades()
        raise NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() < other._get_all_grades()
        raise NotImplemented
    

class Reviewer(Mentor):
    def rate_hw(self, student: Student, course: str, grade: int) -> None:
        """
        метод Ментора, выставляет оценку студенту
        student - должен быть class Student
        course - название курса, курс должен быть как у ментора так и у студента
        grade - оценка
        """
        if isinstance(student, Student):
            if all(map(lambda x: course in x, (student.courses_in_progress, 
                                               self.courses_attached))):
                if isinstance(grade, int) and grade in range(1, 11):
                    student.grades.setdefault(course, []).append(grade)
                    return True
                raise GradeError(f'{grade} не является валидной оценкой')
            raise CourseError(f'{course} не является общим')
        raise TypeError(f'{student.surname} не явлется студентом')

    def __str__(self) -> str:
        return f'Имя: {self.name}\nФамилия: {self.surname}'


def students_eval(stud: Student, lect: Lecturer):
    """
    функция рандомно проставялет оценки лекторам от студентов.
    курсы должны совпадать
    результат выводится на печать и валидные оценки попадают в поле экземпляра
    """
    print(f'общие курсы у {stud.name} и {lect.name}: ', end='')
    print(*set(stud.courses_in_progress)&set(lect.courses_attached))
    for _ in range(20):
        try:
            stud.rate_lecturer(lecturer=lect, course=choice(all_courses),
                                grade=randint(1, 10))
        except (TypeError, GradeError, CourseError): 
            pass
    print('проверим правильность заполнения')
    print(lect.grades_from_stud)
    print('-'*80)
    print(f'проверим правильность заполнения\n'
            f'Оценки лектора {lect.surname}\n'
            f'{lect.surngrades_from_studame}\n'
            f'{"-"*80}')

def reviewer_eval(rev: Reviewer, stud: Student):
    """
    функция рандомно проставялет оценки студентам от экспертов.
    экспрет может оценивать все курсы 
    результат выводится на печать и валидные оценки попадают в поле экземпляра
    """
    print(f'общие курсы у {stud.name} и {rev.name}: ', end='')
    print(*set(rev.courses_attached)&set(stud.courses_in_progress))
    for _ in range(20):
        try:
            rev.rate_hw(student=stud, course=choice(all_courses), 
                        grade=randint(1, 10))
        except (TypeError, GradeError, CourseError): 
            pass            
    print(f'проверим правильность заполнения\n'
        f'Оценки студента {stud.surname}\n'
        f'{stud.grades}\n'
        f'{"-"*80}')

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

    