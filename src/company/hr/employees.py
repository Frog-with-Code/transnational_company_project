from abc import ABC, abstractmethod
from .enums import *
from datetime import date, timedelta
from random import random
from ..common.enums import normalize_enum
from ..finance.budget import Money
from ..common.descriptors import NonNegative
from ..common.exceptions import EmployeePossibilityError


class AbstractEmployee(ABC):
    """
    Abstract base class representing a generic employee in the system.

    Encapsulates core personal and professional details, including salary,
    role, and experience. Implements hashing and equality based on unique IDs.

    Attributes:
        name (str): First name.
        surname (str): Last name.
        personal_id (int): Unique identifier for the employee.
        role (EmployeeRole): Functional role within the company.
        classification (EmployeeClassification): Job grade or tier.
        salary (Money): Financial compensation object.
        experience (int): Years of professional experience (must be non-negative).
    """

    experience = NonNegative()

    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: int,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: Money,
    ) -> None:
        """
        Initialize the AbstractEmployee.

        Args:
            name (str): First name.
            surname (str): Last name.
            personal_id (int): Unique system ID.
            role (EmployeeRole): Employee's role.
            classification (EmployeeClassification): Employee's classification.
            experience (int): Years of experience.
            salary (Money): Compensation.
        """
        self.name = name
        self.surname = surname
        self._personal_id = personal_id
        self.role = role
        self.classification = classification
        self.salary = salary
        self.experience = experience

    def __hash__(self) -> int:
        """Return the hash of the employee's unique ID."""
        return hash(self._personal_id)

    def __eq__(self, other: "AbstractEmployee") -> bool:
        """
        Check equality based on full name and personal ID.

        Args:
            other (AbstractEmployee): The object to compare with.

        Returns:
            bool: True if both are employees with matching ID and name.
        """
        return (
            isinstance(other, AbstractEmployee)
            and self.full_name == other.full_name
            and self.personal_id == other.personal_id
        )

    @abstractmethod
    def work(self):
        """Execute the employee's primary job function (printed to stdout)."""
        pass

    @abstractmethod
    def profession(self):
        """Return the string identifier of the employee's profession."""
        pass

    @abstractmethod
    def can_work_remotely(self) -> bool:
        """
        Check if the employee can perform their duties remotely.

        Returns:
            bool: True if remote work is possible, False otherwise.
        """
        pass

    @property
    def full_name(self) -> str:
        """
        Get the full name of the employee.

        Returns:
            str: "FirstName LastName"
        """
        return f"{self.name} {self.surname}"

    @classmethod
    def get_specific_fields(cls) -> set[str]:
        """
        Get fields specific to the concrete employee subclass.

        Returns:
            set[str]: Set of field names.
        """
        return cls.specific_fields

    @classmethod
    def get_necessary_fields(cls) -> set[str]:
        """
        Get all required fields for initialization (common + specific).

        Returns:
            set[str]: Combined set of field names.
        """
        return cls.common_fields | cls.specific_fields

    @property
    def personal_id(self) -> int:
        """Get the employee's unique ID."""
        return self._personal_id


class OfficeEmployee(AbstractEmployee, ABC):
    """
    Abstract class for employees who work in an office environment.

    Office employees are generally capable of remote work.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def can_work_remotely(self):
        """
        Check remote work capability.

        Returns:
            bool: Always True for office employees.
        """
        return True


class FieldEmployee(AbstractEmployee, ABC):
    """
    Abstract class for employees who work on-site or in the field.

    Attributes:
        workwear (list[str]): Required protective clothing or gear.
        medical_check_date (date): Date of last medical examination.
    """

    def __init__(self, workwear: list[str], medical_check_date: date, **kwargs) -> None:
        super().__init__(**kwargs)
        self.workwear = workwear[:]
        self.medical_check_date = medical_check_date

    def can_work_remotely(self) -> bool:
        """
        Check remote work capability.

        Returns:
            bool: Always False for field employees.
        """
        return False

    def is_medically_fit(self) -> bool:
        """
        Check if the medical examination is still valid (within 1 year).

        Returns:
            bool: True if the check date is within the last 365 days.
        """
        return self.medical_check_date + timedelta(days=365) >= date.today()


class ITSpecialist(OfficeEmployee):
    """
    Represents an IT professional.

    Attributes:
        specialization (ITSpecialization): Area of expertise (e.g., DevOps).
        programming_langs (list[str]): Known programming languages.
        qualification_level (ITQualificationLevel): Seniority level.
        active_projects (set[str]): Currently assigned projects.
    """

    def __init__(
        self,
        *,
        specialization: ITSpecialization | str,
        programming_langs: list[str],
        qualification_level: ITQualificationLevel | str,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.specialization = normalize_enum(specialization, ITSpecialization)
        self.programming_langs = programming_langs[:]
        self.qualification_level = normalize_enum(
            qualification_level, ITQualificationLevel
        )

        self.active_projects: set[str] = set()

    @property
    def profession(self) -> str:
        """Returns 'it_specialist'."""
        return "it_specialist"

    def assign_project(self, project: str) -> None:
        """Add a project to the employee's workload."""
        self.active_projects.add(project)

    def complete_project(self, project: str) -> None:
        """Remove a project from the employee's workload."""
        self.active_projects.discard(project)

    def get_active_projects_amount(self) -> int:
        """Return the count of currently active projects."""
        return len(self.active_projects)

    def work(self):
        """
        Simulate working behavior.

        Output depends on the number of active projects (stress level).
        """
        if self.get_active_projects_amount() < 2:
            print("*Lazy printing*")
        else:
            print("*Pressing keys in panic*")


class Accountant(OfficeEmployee):
    """
    Represents a financial accountant.

    Attributes:
        erp_systems (list[str]): Knowledge of Enterprise Resource Planning systems.
        certifications (list[FinancialQualification]): Professional credentials.
        audit_status (str): Current audit state ("none" or "in_progress").
    """

    def __init__(
        self,
        *,
        erp_systems: list[str],
        certifications: list[FinancialQualification] | list[str],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.erp_systems = erp_systems[:]
        self.certifications = normalize_enum(certifications, FinancialQualification)

        self.audit_status: str = "none"

    @property
    def profession(self) -> str:
        """Returns 'accountant'."""
        return "accountant"

    def can_handle_audit(self) -> bool:
        """
        Check if the accountant holds a certification valid for auditing.

        Valid certifications: CPA, ACCA, CIA.

        Returns:
            bool: True if certified.
        """
        audit_certs = {
            FinancialQualification.CPA,
            FinancialQualification.ACCA,
            FinancialQualification.CIA,
        }
        return any(cert in audit_certs for cert in self.certifications)

    def start_audit(self) -> None:
        """
        Begin an audit process.

        Raises:
            EmployeePossibilityError: If the accountant lacks the required certification.
        """
        if not self.can_handle_audit():
            raise EmployeePossibilityError("Employee can't handle audits")

        self.audit_status = "in_progress"

    def end_audit(self) -> None:
        """
        Finish the current audit.

        Prints a message if no audit was active.
        """
        if self.audit_status == "in_progress":
            self.audit_status = "none"
        else:
            print("There is not active audit")

    def work(self) -> None:
        """Simulate work output."""
        "*Trying to avoid prison*"


class Seller(OfficeEmployee):
    """Represents a sales employee."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def profession(self) -> str:
        """Returns 'seller'."""
        return "seller"

    def work(self) -> None:
        """Simulate sales activity."""
        print("*Trying to sell a pen*")


class HRSpecialist(OfficeEmployee):
    """Represents a Human Resources specialist."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def profession(self) -> str:
        """Returns 'hr_specialist'."""
        return "hr_specialist"

    def work(self) -> None:
        """Simulate HR activity."""
        print("*Talking with some strangers*")


class Driver(FieldEmployee):
    """
    Represents a driver.

    Attributes:
        license_category (str): The class of vehicle the driver can operate.
        license_expire_date (date): Date when the license expires.
        accidents (int): Count of accidents involved in.
        routes (set[str]): Assigned driving routes.
    """

    def __init__(
        self, *, license_category: str, license_expire_date: date, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.license_category = license_category
        self.license_expire_date = license_expire_date

        self.accidents: int = 0
        self.routes: set[str] = set()

    @property
    def profession(self) -> str:
        """Returns 'driver'."""
        return "driver"

    def is_valid_license(self) -> date:
        """
        Check if the driver's license is currently valid.

        Note:
            Return type annotation suggests returning a date, but logic returns bool.
            The docstring reflects the implementation logic.

        Returns:
            bool: True if expiration date is in the future.
        """
        return self.license_expire_date > date.today()

    def work(self) -> None:
        """
        Simulate driving.

        There is a small probability of an accident occurring, inversely
        proportional to experience.
        """
        accident_probability = 1 / (100 * self.experience)
        if random() < accident_probability:
            self.accidents += 1
        print("Wrrooom-wrroom")

    def assign_route(self, routes: str | list[str] | set[str]) -> None:
        """
        Assign one or more routes to the driver.

        Args:
            routes (str | list[str] | set[str]): Route name(s) to add.
        """
        if isinstance(routes, str):
            self.routes.add(routes)
        else:
            self.routes.update(routes)

    def unassign_route(self, routes: str | list[str] | set[str]) -> None:
        """
        Remove one or more routes from the driver.

        Args:
            routes (str | list[str] | set[str]): Route name(s) to remove.
        """
        if isinstance(routes, str):
            self.routes.discard(routes)
        else:
            self.routes.difference_update(routes)


class Cleaner(FieldEmployee):
    """
    Represents a maintenance/cleaning employee.

    Attributes:
        skills (list[str]): Specific cleaning capabilities.
        hazardous_waste_trained (bool): Certification for dangerous waste.
        equipment (set[str]): Currently held tools/equipment.
    """

    def __init__(
        self, *, skills: list[str], hazardous_waste_trained: bool, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.skills = skills[:]
        self.hazardous_waste_trained = hazardous_waste_trained

        self.equipment: set[str] = set()

    @property
    def profession(self) -> str:
        """Returns 'cleaner'."""
        return "cleaner"

    def give_equipment(self, tool: str) -> None:
        """Assign a tool to the cleaner."""
        self.equipment.add(tool)

    def take_equipment(self, tool: str) -> None:
        """Retrieve a tool from the cleaner."""
        self.equipment.discard(tool)

    def has_equipment(self) -> bool:
        """Check if the cleaner has any tools."""
        return len(self.equipment) != 0

    def work(self):
        """
        Simulate cleaning work.

        There is a probability of breaking a tool, inversely proportional to experience.
        """
        broken_tool_probability = 1 / (100 * self.experience)
        if random() < broken_tool_probability and self.has_equipment():
            self.equipment.pop()
        print("*Doing cleaning*")
