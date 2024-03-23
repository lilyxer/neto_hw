class People:
    def __init__(self, name: str, surname: str) -> None:
        self.name = name
        self.surname = surname

    def __str__(self) -> str:
        return f'{self.name}, {self.surname}'


def get_employees(lst_of_peoples: list[People]) -> str:
    return '\n'.join(str(people) for people in lst_of_peoples)