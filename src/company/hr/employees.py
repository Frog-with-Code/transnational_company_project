from abc import ABC, abstractmethod
from .enums import EmployeeClassification, EmployeeRole, ITSpecialization


class AbstractEmployee(ABC):
    specific_fields : set[str] = set()
    
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int,
        **specific_params
    ) -> None:
        self.name = name
        self.surname = surname
        self.personal_id = personal_id
        self.role = role
        self.classification = classification
        self.salary = salary
        self.experience = experience

    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def get_profession(self):
        pass

    def get_fields(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "personal_id": self.id,
            "profession": self.get_profession(),
            "role": self.role,
            "classification": self.classification,
            "salary": self.salary,
        }
        
    def get_full_name(self) -> str:
        return self.name + self.surname
    
    @classmethod
    def get_specific_fields(cls):
        return cls.specific_fields


class Engineer(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self):
        return "engineer"


class ITSpecialist(Engineer):
    specific_fields = {
        "programming_langs",
        "specialization"
    }
    
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int,
        specialization: ITSpecialization | str,
        programming_langs: list[str]
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )
        if isinstance(specialization, str):
            self.specialization = ITSpecialization(specialization)
        else : self.specialization = specialization
        self.programming_langs = programming_langs
        

    def get_profession(self) -> str:
        return "it_specialist"
    
    def work(self):
        print("Do some staff")


class Accountant(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self) -> str:
        return "accountant"


class Seller(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self) -> str:
        return "seller"


class HRSpecialist(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self) -> str:
        return "hr_specialist"


class Driver(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self) -> str:
        return "driver"


class Cleaner(AbstractEmployee):
    def __init__(
        self,
        *,
        name: str,
        surname: str,
        personal_id: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: int
    ) -> None:
        super().__init__(
            name=name,
            surname=surname,
            personal_id=personal_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
        )

    def get_profession(self) -> str:
        return "cleaner"
