from .hr import *
from .company_structure import *
from .finance import *
from .logistics import *
from products import *

def __main__():
    emp = EmployeeFactory().create_from_file("/home/frog/py_projects/transnational_company_project/src/company/employee.json")
    print(emp.get_fields())
    print("hi")
    
if __name__ == "__main__":
    __main__()