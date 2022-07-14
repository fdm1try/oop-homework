from random import randint, choice


class ValidationError(Exception):
    pass


class Person:
    def __init__(self, name, surname, gender=None):
        self.name = name
        self.surname = surname
        self.gender = gender


class Gradeable():
    def avg_grade(self, course_to_grade=None):
        grades = [
            sum(grade_list) / len(grade_list)
            for course, grade_list in self.grades.items()
            if course_to_grade is None or course == course_to_grade
        ]
        return None if not len(grades) else round(sum(grades) / len(grades), 1)

    def __gt__(self, other):
        if not isinstance(other, Gradeable):
            raise ValidationError('Нельзя сравнить разные типы.')
        return self.avg_grade() > other.avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Gradeable):
            raise ValidationError('Нельзя сравнить разные типы.')
        return self.avg_grade() == other.avg_grade()


class Student(Person, Gradeable):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lection(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise ValidationError('Студент может оценивать только лекторов.')
        if course not in self.courses_in_progress or course not in lecturer.courses_attached:
            raise ValidationError('Студент или лектор не закреплён к указанному курсу.')
        lecturer.grades[course] = lecturer.grades[course] + [grade] if course in lecturer.grades else [grade]

    def __str__(self):
        avg_grade = self.avg_grade()
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {avg_grade if avg_grade is not None else "нет оценок"}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}'
        )


class Mentor(Person):
    def __init__(self, name, surname, gender=None):
        super().__init__(name, surname, gender)
        self.courses_attached = []


class Lecturer(Mentor, Gradeable):
    def __init__(self, name, surname, gender=None):
        super().__init__(name, surname, gender)
        self.grades = {}

    def __str__(self):
        avg_grade = self.avg_grade()
        return (
            f'Имя: {self.name}\nФамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {avg_grade if avg_grade is not None else "нет оценок"}'
        )


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            raise ValidationError('Оценку можно поставить только студенту.')
        if course not in self.courses_attached or course not in student.courses_in_progress:
            raise ValidationError('Студент или лектор не закреплён к указанному курсу.')
        student.grades[course] = student.grades[course] + [grade] if course in student.grades else [grade]

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


courses = ['Python', 'Javascript', 'HTML', 'CSS', 'GIT']
names = ['Александр', 'Вероника', 'Иван', 'Анжелика', 'Николай', 'Клубника', 'Евгений', 'Эвелина', 'Пётр', 'Лика', 'Виктор', 'Вика']
surnames = ['Иванов', 'Николаев', 'Александров', 'Логинов', 'Паролев', 'Вебов', 'Питонов', 'Стилев', 'Скриптов', 'Вариэйблов']


def gen_person():
    name = choice(names)
    surname = choice(surnames)
    gender = 'женский' if name.endswith('а') else 'мужской'
    if gender == 'женский':
        surname += 'а'
    return name, surname, gender


def avg_grade_students(students, course):
    grades = [student.avg_grade(course) for student in students if isinstance(student, Student)]
    return sum(grades) / len(grades)


def avg_grade_lecturers(lecturers, course):
    grades = [lecturer.avg_grade(course) or 0 for lecturer in lecturers if isinstance(lecturer, Lecturer)]
    return sum(grades) / len(grades)


if __name__ == '__main__':
    # зачисление студентов
    student_frontend = Student(*gen_person())
    student_frontend.courses_in_progress = ['HTML', 'CSS', 'Javascript', 'GIT']
    student_backend = Student(*gen_person())
    student_backend.courses_in_progress = ['Python', 'SQL', 'GIT']
    # найм преподавателей
    reviewer_frontend = Reviewer(*gen_person())
    reviewer_frontend.courses_attached = ['HTML', 'CSS', 'Javascript', 'GIT']
    reviewer_backend = Reviewer(*gen_person())
    reviewer_backend.courses_attached = ['Python', 'SQL', 'GIT']
    lecturer_frontend = Lecturer(*gen_person())
    lecturer_frontend.courses_attached = ['HTML', 'CSS', 'Javascript', 'GIT']
    lecturer_backend = Lecturer(*gen_person())
    lecturer_backend.courses_attached = ['Python', 'SQL', 'GIT']
    # оценка лекций
    student_frontend.rate_lection(lecturer_frontend, 'HTML', randint(1, 10))
    student_frontend.rate_lection(lecturer_frontend, 'Javascript', randint(1, 10))
    student_frontend.rate_lection(lecturer_backend, 'GIT', randint(1, 10))
    student_backend.rate_lection(lecturer_backend, 'Python', randint(1, 10))
    student_backend.rate_lection(lecturer_backend, 'SQL', randint(1, 10))
    student_backend.rate_lection(lecturer_frontend, 'GIT', randint(1, 10))
    # оценка студентов
    reviewer_frontend.rate_hw(student_frontend, 'HTML', randint(1, 10))
    student_frontend.finished_courses.append('HTML')
    student_frontend.courses_in_progress.remove('HTML')
    reviewer_frontend.rate_hw(student_frontend, 'Javascript', randint(1, 10))
    student_frontend.finished_courses.append('Javascript')
    student_frontend.courses_in_progress.remove('Javascript')
    reviewer_frontend.rate_hw(student_frontend, 'GIT', randint(1, 10))
    reviewer_backend.rate_hw(student_frontend, 'GIT', randint(1, 10))
    student_frontend.finished_courses.append('GIT')
    student_frontend.courses_in_progress.remove('GIT')
    reviewer_backend.rate_hw(student_backend, 'Python', randint(1, 10))
    student_backend.finished_courses.append('Python')
    student_backend.courses_in_progress.remove('Python')
    reviewer_backend.rate_hw(student_backend, 'GIT', randint(1, 10))
    reviewer_frontend.rate_hw(student_backend, 'GIT', randint(1, 10))
    student_backend.finished_courses.append('GIT')
    student_backend.courses_in_progress.remove('GIT')
    # работа с остальными методами и функциями
    if student_backend == student_frontend:
        print(f'Лучшие студенты:\n{student_frontend}\n\n{student_backend}')
    else:
        best_student = student_backend if student_backend > student_frontend else student_frontend
        print(f'Лучший студент:\n{best_student}')
    print('-'*40)
    if lecturer_backend == lecturer_frontend:
        print(f'Лучшие лекторы:\n{lecturer_frontend}\n\n{lecturer_backend}')
    else:
        best_lecturer = lecturer_frontend if lecturer_backend < lecturer_frontend else lecturer_backend
        print(f'Лучший лектор:\n{best_lecturer}')
    print('-' * 40)
    print(f'Средняя оценка лекций по курсу GIT: {avg_grade_lecturers([lecturer_frontend, lecturer_backend], "GIT")}')
    print(f'Средняя оценка ДЗ по курсу GIT: {avg_grade_students([student_frontend, student_backend], "GIT")}')
