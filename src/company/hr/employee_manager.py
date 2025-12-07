from .employees import AbstractEmployee
from ..common.exceptions import (
    EmployeeAlreadyHiredError,
    EmployeeNotHiredError,
)
from ..finance.budget import Money


class EmployeeManagerMixin:
    """
    Mixin that provides employee management capabilities to a class.

    This mixin allows any class (like `Department`, `Transport`, or `Warehouse`) to
    maintain a set of employees, handle hiring/firing logic, and calculate total
    payroll costs. It expects the host class to initialize `self._employees` as a set.

    Attributes:
        _employees (set[AbstractEmployee]): Internal storage of assigned employees.
    """

    @property
    def employees(self) -> set[AbstractEmployee]:
        """
        Get a copy of the current set of employees.

        Returns:
            set[AbstractEmployee]: A copy of the internal employee set to prevent
            direct external modification of the roster.
        """
        return self._employees.copy()

    def hire(self, employee: AbstractEmployee) -> None:
        """
        Add an employee to the roster.

        Args:
            employee (AbstractEmployee): The employee to hire.

        Raises:
            EmployeeAlreadyHiredError: If the employee is already in the roster.
        """
        if self.has_employee(employee):
            print(f"{employee.full_name} is already employed!")
            raise EmployeeAlreadyHiredError(employee.full_name)

        self._employees.add(employee)
        print(f"{employee.full_name} was successfully hired")

    def fire(self, employee: AbstractEmployee) -> None:
        """
        Remove an employee from the roster.

        Args:
            employee (AbstractEmployee): The employee to remove.

        Raises:
            EmployeeNotHiredError: If the employee is not currently in the roster.
        """
        if not self.has_employee(employee):
            raise EmployeeNotHiredError(employee.full_name)

        self._employees.remove(employee)
        print(f"{employee.full_name} was successfully fired")

    def has_employee(self, employee: AbstractEmployee) -> bool:
        """
        Check if a specific employee is currently in the roster.

        Args:
            employee (AbstractEmployee): The employee to check.

        Returns:
            bool: True if the employee is present, False otherwise.
        """
        return employee in self._employees

    def calculate_payroll(self) -> Money:
        """
        Calculate the total cost of salaries for all employees in this unit.

        Iterates through all employees and sums their salaries.

        Returns:
            Money: The total sum of all salaries.

        Raises:
            DifferentCurrenciesError: If employees have salaries in conflicting currencies
                (raised by the Money addition operation).
        """
        total_payroll = Money()
        for employee in self._employees:
            total_payroll += employee.salary
        return total_payroll
