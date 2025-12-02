from employees import AbstractEmployee
from ..common.exceptions import (
    EmployeeAlreadyHiredError,
    EmployeeNotHiredError,
    DifferentCurrenciesError,
)
from ..finance.budget import Money


class EmployeeManagerMixin:
    @property
    def employees(self) -> set[AbstractEmployee]:
        return self._employees.copy()

    def hire(self, employee: AbstractEmployee) -> None:
        if self.has_employee(employee):
            print(f"{employee.full_name} is already employed!")
            raise EmployeeAlreadyHiredError(employee.full_name)

        self._employees.add(employee)
        print(f"{employee.full_name} was successfully hired")

    def fire(self, employee: AbstractEmployee) -> None:
        if not self.has_employee(employee):
            raise EmployeeNotHiredError(employee.full_name)

        self._employees.remove(employee)
        print(f"{employee.full_name} was successfully fired")

    def has_employee(self, employee: AbstractEmployee) -> bool:
        return employee in self._employees

    def calculate_payroll(self) -> Money:
        total_payroll = Money()
        for employee in self._employees:
            total_payroll += employee.salary
        return total_payroll
