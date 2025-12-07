NonNegative 0 3 ->

Region 6 0 ->

Location 5 1 -> Region

AbstractCompany 5 6 -> Location, AbstractEmployee, Budget

HeadquarterCompany 2 6 -> SubsidiaryCompany, AssociatedCompany

SubsidiaryCompany 2 4 -> HeadquarterCompany

AssociatedCompany 2 3 -> HeadquarterCompany

BudgetManagementService 2 5 -> CurrencyService

Currency 3 0 ->

Money 2 12 -> Currency

Budget 1 6 -> Money

CurrencyService 2 3 -> Currency

TransactionType 3 0 ->

TransactionStatus 3 0 ->

Transaction 9 1 -> TransactionType, TransactionStatus, Money, AbstractCompany

BaseEmployeeSchema 6 0 -> EmployeeRole, EmployeeClassification, Money

FieldEmployeeSchema 2 0 ->

ITSpecialistSchema 4 0 -> ITSpecialization, ITQualification

DriverSchema 3 0 -> 

AccountantSchema 3 0 -> FinancialQualification

SellerSchema 1 0 ->

HRSpecialistSchema 1 0 ->

CleanerSchema 3 0 ->

EmployeeFactory 3 1 -> ITSpecialist, DriverSchema, SellerSChema, HRSpecialistSchema, CleanerSchema

EmployeeManagerMixin 0 5 -> AbstractEmployee, Money

AbstractEmployee 8 10 -> EmployeeRole, EmployeeClassification, Money, NonNegative

OfficeEmployee 0 2 -> 

FieldEmployee 2 3 ->

ITSpecialist 4 5 -> ITSpecialization, ITQualification

Accountant 3 5 -> FinancialQualification

Seller 0 3 ->

HRSpecialist 0 3 ->

Driver 4 5 ->

Cleaner 3 5 -> 

EmployeeRole 6 0 ->

EmployeeClassification 9 0 ->

ITSpecialization 10 0 ->

FinancialQualification 6 0 ->

ITQualificationLevel 3 0 ->

CargoManager 3 11 -> NonNegative, AbstractProduct

TransportStatus 6 0 ->

ShipType 5 0 ->

CarFuelType 3 0 ->

BaseTransportSchema 9 0 -> Location

TrainSchema 3 0 -> Wagon

PlaneSchema 4 0 ->

CarSchema 3 0 -> CarFuelType

ShipSchema 3 0 -> ShipType

TransportFactory 2 1 -> Train, Car, Plane, Ship

AbstractTransport 12 12 -> Location, CargoManager, TransportStatus, AbstractEmployee, NonNegative

Wagon 2 1 -> 

Train 3 6 -> Wagon, NonNegative

Plane 3 3 -> NonNegative

Car 2 2 -> CarFuelType

Ship 2 2 -> ShipType, NonNegative

Warehouse 4 6 -> AbstractEmployee, CargoManager, NonNegative

AbstractProduct 3 1 -> 

<br>

**Exceptions(14):**

DifferentCurrenciesError 0 0 ->

ForbiddenTransactionError 0 0 ->

InsufficientBudgetError 0 0 ->

EmployeeError 0 0 ->

EmployeeAlreadyHiredError 0 1 ->

EmployeeNotHiredError 0 1 ->

EmployeePossibilityError 0 0 ->

CompanyError 0 0 ->

CompanyAlreadyCooperatedError 0 0 ->

CompanyNotCooperatedError 0 0 ->

CompanyOwnershipStakeError 0 0 ->

CargoError 0 0 ->

ImpossibleLoading 0 0 ->

ImpossibleUnloading 0 0 ->
    
<br>

**Классы: 71,
Поля: 203,
Поведения: 144,
Ассоциации: 60,
Исключения: 14**



