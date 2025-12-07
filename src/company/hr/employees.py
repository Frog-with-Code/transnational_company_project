from abc import ABC, abstractmethod
from .enums import *
from datetime import date, timedelta
from random import random
from ..common.enums import normalize_enum
from ..finance.budget import Money
from ..common.descriptors import NonNegative
from ..common.exceptions import EmployeePossibilityError


class AbstractEmployee(ABC):
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
        self.name = name
        self.surname = surname
        self._personal_id = personal_id
        self.role = role
        self.classification = classification
        self.salary = salary
        self.experience = experience

    def __hash__(self) -> int:
        return hash(self._personal_id)

    def __eq__(self, other: "AbstractEmployee") -> bool:
        return (
            isinstance(other, AbstractEmployee)
            and self.full_name == other.full_name
            and self.personal_id == other.personal_id
        )

    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def profession(self):
        pass

    @abstractmethod
    def can_work_remotely(self) -> bool:
        pass

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.surname}"

    @classmethod
    def get_specific_fields(cls) -> set[str]:
        return cls.specific_fields

    @classmethod
    def get_necessary_fields(cls) -> set[str]:
        return cls.common_fields | cls.specific_fields

    @property
    def personal_id(self) -> int:
        return self._personal_id


class OfficeEmployee(AbstractEmployee, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def can_work_remotely(self):
        return True


class FieldEmployee(AbstractEmployee, ABC):
    def __init__(self, workwear: list[str], medical_check_date: date, **kwargs) -> None:
        super().__init__(**kwargs)
        self.workwear = workwear[:]
        self.medical_check_date = medical_check_date

    def can_work_remotely(self) -> bool:
        return False

    def is_medically_fit(self) -> bool:
        return self.medical_check_date + timedelta(days=365) >= date.today()


class ITSpecialist(OfficeEmployee):
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
        return "it_specialist"

    def assign_project(self, project: str) -> None:
        self.active_projects.add(project)

    def complete_project(self, project: str) -> None:
        self.active_projects.discard(project)

    def get_active_projects_amount(self) -> int:
        return len(self.active_projects)

    def work(self):
        if self.get_active_projects_amount() < 2:
            print("*Lazy printing*")
        else:
            print("*Pressing keys in panic*")


class Accountant(OfficeEmployee):
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
        return "accountant"

    def can_handle_audit(self) -> bool:
        audit_certs = {
            FinancialQualification.CPA,
            FinancialQualification.ACCA,
            FinancialQualification.CIA,
        }
        return any(cert in audit_certs for cert in self.certifications)

    def start_audit(self) -> bool:
        if not self.can_handle_audit():
            raise EmployeePossibilityError("Employee can't handle audits")

        self.audit_status = "in_progress"

    def end_audit(self) -> None:
        if self.audit_status == "in_progress":
            self.audit_status = "none"
        else:
            print("There is not active audit")

    def work(self):
        "*Trying to avoid prison*"


class Seller(OfficeEmployee):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def profession(self) -> str:
        return "seller"

    def work(self) -> None:
        print("*Trying to sell a pen*")


class HRSpecialist(OfficeEmployee):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def profession(self) -> str:
        return "hr_specialist"

    def work(self) -> None:
        print("*Talking with some strangers*")


class Driver(FieldEmployee):
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
        return "driver"

    def is_valid_license(self) -> date:
        return self.license_expire_date > date.today()

    def work(self) -> None:
        accident_probability = 1 / (100 * self.experience)
        if random() < accident_probability:
            self.accidents += 1
        print("Wrrooom-wrroom")

    def assign_route(self, routes: str | list[str] | set[str]) -> None:
        if isinstance(routes, str):
            self.routes.add(routes)
        else:
            self.routes.update(routes)

    def unassign_route(self, routes: str | list[str] | set[str]) -> None:
        if isinstance(routes, str):
            self.routes.discard(routes)
        else:
            self.routes.difference_update(routes)


class Cleaner(FieldEmployee):
    def __init__(
        self, *, skills: list[str], hazardous_waste_trained: bool, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.skills = skills[:]
        self.hazardous_waste_trained = hazardous_waste_trained

        self.equipment: set[str] = set()

    @property
    def profession(self) -> str:
        return "cleaner"

    def give_equipment(self, tool: str) -> None:
        self.equipment.add(tool)

    def take_equipment(self, tool: str) -> None:
        self.equipment.discard(tool)

    def has_equipment(self) -> bool:
        return len(self.equipment) != 0

    def work(self):
        broken_tool_probability = 1 / (100 * self.experience)
        if random() < broken_tool_probability and self.has_equipment():
            self.equipment.pop()
        print("*Doing cleaning*")
