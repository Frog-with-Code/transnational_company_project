from .employees import *
from .enums import EmployeeClassification, EmployeeRole
from pathlib import Path
import json
from ..finance.budget import Money


class EmployeeFactory:
    last_id = 1
    
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
        **specific_params
    ) -> AbstractEmployee:

        self.params_validator.validation()
        employee_class = EmployeeFactory.professions[profession]
        
        required_fields = employee_class.get_specific_fields()
        provided_fields = set(specific_params.keys())
        if required_fields - provided_fields:
            #TODO specific exception
            pass
        
        EmployeeFactory.last_id += 1
        return employee_class(
            name=name,
            surname=surname,
            personal_id=EmployeeFactory.last_id,
            role=role,
            classification=classification,
            experience=experience,
            salary=salary,
            **specific_params
        )

    def create_from_file(self, abs_path: Path) -> AbstractEmployee:
        #self.file_validator.validation()
        with open(abs_path) as f:
            data = json.load(f)["employee"]
        role = EmployeeRole(data["role"])
        classification = EmployeeClassification(data["classification"])
        employee_class = EmployeeFactory.professions[data["profession"]]

        required_fields = employee_class.get_necessary_fields()
        provided_fields = set(data.keys())
        provided_fields.remove("profession")
        specific_fields = employee_class.get_specific_fields()
        if required_fields - provided_fields:
            raise ValueError
        specific_params = {key: data[key] for key in specific_fields}

        EmployeeFactory.last_id += 1
        return employee_class(
            name=data["name"],
            surname=data["surname"],
            personal_id=EmployeeFactory.last_id,
            role=role,
            classification=classification,
            experience=data["experience"],
            salary=data["salary"],
            **specific_params
        )
