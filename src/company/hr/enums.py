from enum import Enum

class EmployeeRole(Enum):
    STAFF = "Staff"
    TEAM_LEAD = "Team Lead"
    MANAGER = "Manager"
    SENIOR_MANAGER = "Senior Manager"
    DIRECTOR = "Director"
    CEO = "CEO"
    
class EmployeeClassification(Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    TEMPORARY = "Temporary"
    SEASONAL = "Seasonal"
    FREELANCE = "Freelance"
    INTERN = "Intern"
    CONTRACT = "Contract"
    VOLUNTEER = "Volunteer"
    ON_CALL = "On-call"
    
class ITSpecialization(Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    FULLSTACK = "Full-stack"
    ML = "ML"
    DEVOPS = "DevOps"
    QA = "QA"
    MOBILE = "Mobile"
    CLOUD = "Cloud"
    DATA = "Data"
    SECURITY = "Security"
    