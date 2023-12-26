from functools import total_ordering


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
        grades: dict - словарь с оценками от студентов по общему курсу {'python': []}
        """
        super().__init__(name, surname)
        self.grades = {}

    def _get_all_grades(self) -> float|None:
        """
        метод лектора, собирает все оценки по всем предметам 
        в один массив и возвращает среднее если есть хотя бы одна оценка
        """
        all_grades = []
        if self.grades:
            for x in self.grades.values():
                all_grades.extend(x)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

    def __str__(self) -> str:
        mean = self._get_all_grades()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {mean}'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() == other._get_all_grades()
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() < other._get_all_grades()
        return NotImplemented


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

    def rate_lecturer(self, lecturer: Lecturer, course: str, grade: int) -> bool|str:
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
                    lecturer.grades.setdefault(course, []).append(grade)
                    return True
                return f'{grade} не является валидной оценкой'
            return f'{course} не является общим'
        return f'{lecturer.surname} не явлется лектором'


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
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, self(type)): 
            return self._get_all_grades() < other._get_all_grades()
        return NotImplemented
    

class Reviewer(Mentor):
    def rate_hw(self, student: Student, course: str, grade: int) -> bool|str:
        """
        метод эксперта, выставляет оценку студенту
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
                return f'{grade} не является валидной оценкой'
            return f'{course} не является общим'
        return f'{student.surname} не явлется студентом'

    def __str__(self) -> str:
        return f'Имя: {self.name}\nФамилия: {self.surname}'

