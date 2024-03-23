from dataclasses import dataclass


@dataclass
class Salary:
    ammount: int

    def calculate_salary(self, percent: int) -> float:
        return round(self.ammount * percent / 100, 2)