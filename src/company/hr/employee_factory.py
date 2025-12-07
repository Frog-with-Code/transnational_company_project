from typing import Literal, Union, Annotated
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from .employees import *
from .enums import EmployeeClassification, EmployeeRole
from ..finance.budget import Money


class BaseEmployeeSchema(BaseModel):
    """
    Foundation Pydantic model for all employee validation schemas.

    Configured to allow arbitrary types to support the custom `Money` class.

    Attributes:
        name (str): First name of the employee (min length 1).
        surname (str): Last name of the employee (min length 1).
        role (EmployeeRole): Functional role within the organization hierarchy.
        classification (EmployeeClassification): Job tier/classification.
        experience (int): Years of experience (must be non-negative).
        salary (Money): Financial object representing the employee's compensation.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    role: EmployeeRole
    classification: EmployeeClassification
    experience: int = Field(..., ge=0)
    salary: Money


class OfficeEmployeeSchema(BaseEmployeeSchema):
    """
    Base schema for office-based personnel. 
    Currently identical to BaseEmployeeSchema but serves as a logical parent.
    """
    pass


class FieldEmployeeSchema(BaseEmployeeSchema):
    """
    Base schema for field workers or operational staff.

    Attributes:
        workwear (list[str]): List of required protective clothing or uniforms.
        medical_check_date (date): Date of the last medical examination.
    """
    workwear: list[str]
    medical_check_date: date


class ITSpecialistSchema(OfficeEmployeeSchema):
    """
    Schema for validating IT Specialist data.

    Attributes:
        profession (Literal["it_specialist"]): Discriminator field.
        programming_langs (list[str]): List of known programming languages.
        specialization (ITSpecialization | str): Specific tech domain (e.g., DevOps, Backend).
        qualification_level (ITQualificationLevel | str): Seniority level (e.g., Junior, Senior).
    """
    profession: Literal["it_specialist"]
    programming_langs: list[str]
    specialization: ITSpecialization | str
    qualification_level: ITQualificationLevel | str


class DriverSchema(FieldEmployeeSchema):
    """
    Schema for validating Driver data.

    Attributes:
        profession (Literal["driver"]): Discriminator field.
        license_category (str): The category of driver's license held (e.g., "C", "D").
        license_expire_date (date): Expiration date of the license.
    """
    profession: Literal["driver"]
    license_category: str
    license_expire_date: date


class AccountantSchema(OfficeEmployeeSchema):
    """
    Schema for validating Accountant data.

    Attributes:
        profession (Literal["accountant"]): Discriminator field.
        erp_systems (list[str]): List of known ERP software (e.g., SAP, 1C).
        certifications (list[FinancialQualification]): Professional financial certifications.
    """
    profession: Literal["accountant"]
    erp_systems: list[str]
    certifications: list[FinancialQualification]


class SellerSchema(OfficeEmployeeSchema):
    """
    Schema for validating Seller data.

    Attributes:
        profession (Literal["seller"]): Discriminator field.
    """
    profession: Literal["seller"]


class HRSpecialistSchema(OfficeEmployeeSchema):
    """
    Schema for validating HR Specialist data.

    Attributes:
        profession (Literal["hr_specialist"]): Discriminator field.
    """
    profession: Literal["hr_specialist"]


class CleanerSchema(FieldEmployeeSchema):
    """
    Schema for validating Cleaner/Janitorial data.

    Attributes:
        profession (Literal["cleaner"]): Discriminator field.
        skills (list[str]): Specific cleaning skills or equipment expertise.
        hazardous_waste_trained (bool): Whether the employee is certified to handle hazardous waste.
    """
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
"""
Union type allowing polymorphic validation based on the 'profession' field.
"""


class EmployeeFactory:
    """
    Factory class for validating input data and creating concrete Employee objects.

    Attributes:
        last_id (int): Class-level counter used to assign unique IDs to new employees.
        validator (TypeAdapter): Pydantic adapter for the `EmployeeInput` union.
        professions (dict): Mapping of profession strings to concrete Employee classes.
    """
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
        """
        Create a specific employee instance based on validated parameters.

        This method combines common arguments with `specific_params` into a single
        dictionary, validates it against the appropriate schema (determined by `profession`),
        and then instantiates the corresponding domain class.

        Args:
            name (str): First name.
            surname (str): Last name.
            profession (str): The key identifying the employee type (e.g., "driver").
            role (EmployeeRole): The role enum value.
            classification (EmployeeClassification): The classification enum value.
            experience (int): Years of experience.
            salary (Money): Salary object.
            **specific_params: Additional keyword arguments required for the specific profession.

        Returns:
            AbstractEmployee: An instance of a concrete employee subclass.

        Raises:
            ValueError: If validation fails (wraps Pydantic ValidationError).
        """
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
