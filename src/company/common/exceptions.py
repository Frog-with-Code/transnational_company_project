class DifferentCurrenciesError(Exception):
    """Exception for financial operations with different currencies"""
    
class ForbiddenTransactionError(Exception):
    """Exception for incorrect parameters in transaction"""
    
class EmployeeError(Exception):
    """Exception for employee-related operations"""
    
class EmployeeAlreadyHiredError(EmployeeError):
    """Raised when trying to hire an employee who is already in the company"""
    def __init__(self, employee_name: str):
        self.message = f"Employee '{employee_name}' is already hired"
        super().__init__(self.message)
    
class EmployeeNotHiredError(EmployeeError):
    """Raised when trying to fire an employee who is not in the company yet"""
    def __init__(self, employee_name: str):
        self.message = f"Employee '{employee_name}' is not hired yet"
        super().__init__(self.message)
        
class CompanyError(Exception):
    """Exception for company related operations"""
    
class CompanyAlreadyCooperatedError(CompanyError):
    """Raised when trying to start cooperation when it's already started"""
    
class CompanyNotCooperatedError(CompanyError):
    """Raised when trying to end cooperation when it's not started yet"""
    
class CompanyOwnershipStakeError(CompanyError):
    """Raised when ownership stake is forbidden for the class"""
    
class CargoError(Exception):
    """Exception for cargo related operations"""
    
class ImpossibleLoading(CargoError):
    """Raised when it's impossible to load cargo on transport"""
    
class ImpossibleUnloading(CargoError):
    """Raised when it's impossible to unload cargo on transport"""
    