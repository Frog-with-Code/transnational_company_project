from typing import Literal, Union, Annotated
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from .employees import *
from .enums import EmployeeClassification, EmployeeRole
from ..finance.budget import Money


class BaseEmployeeSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    role: EmployeeRole
    classification: EmployeeClassification
    experience: int = Field(..., ge=0)
    salary: Money


class OfficeEmployeeSchema(BaseEmployeeSchema):
    pass


class FieldEmployeeSchema(BaseEmployeeSchema):
    workwear: list[str]
    medical_check_date: date


class ITSpecialistSchema(OfficeEmployeeSchema):
    profession: Literal["it_specialist"]
    programming_langs: list[str]
    specialization: ITSpecialization | str
    qualification_level: ITQualificationLevel | str


class DriverSchema(FieldEmployeeSchema):
    profession: Literal["driver"]
    license_category: str
    license_expire_date: date


class AccountantSchema(OfficeEmployeeSchema):
    profession: Literal["accountant"]
    erp_systems: list[str]
    certifications: list[FinancialQualification]


class SellerSchema(OfficeEmployeeSchema):
    profession: Literal["seller"]


class HRSpecialistSchema(OfficeEmployeeSchema):
    profession: Literal["hr_specialist"]


class CleanerSchema(FieldEmployeeSchema):
    profession: Literal["cleaner"]
    skills: list[str]
    hazardous_waste_trained: bool


EmployeeInput = Annotated[
    Union[
        ITSpecialistSchema,
        DriverSchema,
        AccountantSchema,
        SellerSchema,
        HRSpecialistSchema,
        CleanerSchema,
    ],
    Field(discriminator="profession"),
]


class EmployeeFactory:
    last_id = 1
    validator = TypeAdapter(EmployeeInput)

    professions = {
        "it_specialist": ITSpecialist,
        "accountant": Accountant,
        "seller": Seller,
        "hr_specialist": HRSpecialist,
        "driver": Driver,
        "cleaner": Cleaner,
    }

    def create_by_params(
        self,
        name: str,
        surname: str,
        profession: str,
        role: EmployeeRole,
        classification: EmployeeClassification,
        experience: int,
        salary: Money,
        **specific_params,
    ) -> AbstractEmployee:

        raw_data = {
            "name": name,
            "surname": surname,
            "profession": profession,
            "role": role,
            "classification": classification,
            "experience": experience,
            "salary": salary,
            **specific_params,
        }
        try:
            model = self.validator.validate_python(raw_data)
            valid_data = model.model_dump()

        except ValidationError as e:
            raise ValueError(f"Impossible to create employee: {e}")

        profession = valid_data.pop("profession")
        employee_class = self.professions[profession]

        EmployeeFactory.last_id += 1

        return employee_class(personal_id=EmployeeFactory.last_id, **valid_data)
