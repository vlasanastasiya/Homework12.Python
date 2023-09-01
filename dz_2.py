import csv
from functools import reduce
from pathlib import Path


class Validate:
   

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def validate(self, value):
        if not value.isalpha():
            raise TypeError(f'{value} должен содержать только буквы')
        if not value.istitle():
            raise TypeError(f'{value} должен начинаться с заглавной буквы')


class Student:
    name = Validate()
    last_name = Validate()
    surname = Validate()
    _lessons = None

    def __init__(self, name: str, last_name: str, surname: str, lessons_file: Path):
        self.name = name
        self.last_name = last_name
        self.surname = surname
        self.lessons = lessons_file

    @property
    def lessons(self):
        return self._lessons

    @lessons.setter
    def lessons(self, lessons_file: Path):
        

        self._lessons = {"lessons": {}}
        with open(lessons_file, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self._lessons["lessons"][row[0]] = {"assessments": [], "test_results": [], "average_test": None}
        self._lessons["middle_assessment"] = None
        self._lessons["middle_test"] = None

    def __call__(self, lesson: str, number: int, type_est: str = "lesson"):
        

        if lesson not in self.lessons["lessons"].keys():
            raise AttributeError("Такого предмета нет")
        if type_est == "lesson":
            if number < 2 or number > 5:
                raise ValueError("Оценка не может быть меньше 2 и больше 5")
            self.lessons["lessons"][lesson]["assessments"].append(number)
            self.lessons["middle_assessment"] = self.average(self.lessons)
        elif type_est == "test":
            if number < 0 or number > 100:
                raise ValueError("Оценка должна быть от 0 до 100")
            self.lessons["lessons"][lesson]["test_results"].append(number)

           
            self.lessons["lessons"][lesson]["average_test"] = reduce(lambda x, y: x + y, self.lessons["lessons"][lesson]["test_results"]) / len(self.lessons["lessons"][lesson]["test_results"])
            self.lessons['middle_test'] = self.average_ball(self.lessons)

    @staticmethod
    def average(lessons: dict) -> float:
        

        all_estimates = []
        [all_estimates.extend(lessons["lessons"][name]["assessments"]) for name in lessons["lessons"]]

        return reduce(lambda x, y: x + y, all_estimates) / len(all_estimates)

    @staticmethod
    def average_ball(lessons: dict) -> float:
        

        all_estimates = []
        [all_estimates.extend(lessons["lessons"][name]["test_results"]) for name in lessons["lessons"]]

        return reduce(lambda x, y: x + y, all_estimates) / len(all_estimates)

    def __repr__(self):
        result = f'ФИО студента = {self.name} {self.last_name} {self.surname}\nСредняя оценка по всем предметам = {self.lessons["middle_assessment"]}\nСредний бал по всем тестам = {self.lessons["middle_test"]}\n'
        result += "\nОценки по предметам:\n"

        for key, value in self.lessons["lessons"].items():
            result += f'{key} = {value["assessments"]}\n'
        result += "\nТесты по предметам:\n"
        for key, value in self.lessons["lessons"].items():
            result += f'{key} = {value["test_results"]}, средний бал = {value["average_test"]}\n'

        return result


if __name__ == '__main__':
    student = Student("Nikolay", "Ivanovich", "Petrov", Path('lessons.csv'))
    student("русский язык", 5)
    student("русский язык", 5)
    student("математика", 5)
    student("математика", 4)
    student("химия", 3)
    student("химия", 89, "test")
    student("физика", 3)
    student("история", 4)
    student("история", 56, "test")
    print(student)

    