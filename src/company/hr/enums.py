from enum import Enum


class EmployeeRole(Enum):
    """
    Hierarchical roles within the organization.

    Values:
        STAFF: General individual contributor.
        TEAM_LEAD: Leader of a specific team or unit.
        MANAGER: Manager of a department or group of teams.
        SENIOR_MANAGER: Higher-level management overseeing other managers.
        DIRECTOR: Head of a division or major function.
        CEO: Chief Executive Officer.
    """

    STAFF = "Staff"
    TEAM_LEAD = "Team Lead"
    MANAGER = "Manager"
    SENIOR_MANAGER = "Senior Manager"
    DIRECTOR = "Director"
    CEO = "CEO"


class EmployeeClassification(Enum):
    """
    Types of employment contracts and work arrangements.

    Values:
        FULL_TIME: Standard permanent employment (usually 40h/week).
        PART_TIME: Permanent employment with reduced hours.
        TEMPORARY: Employment for a limited duration.
        SEASONAL: Employment during specific seasons or peak periods.
        FREELANCE: Self-employed contractor working on specific projects.
        INTERN: Student or trainee working for experience.
        CONTRACT: Fixed-term contract employment.
        VOLUNTEER: Unpaid work.
        ON_CALL: Employment where work is performed only when requested.
    """

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
    """
    Technical domains and specializations for IT specialists.

    Values:
        FRONTEND: Client-side web development.
        BACKEND: Server-side logic and database integration.
        FULLSTACK: Combination of frontend and backend development.
        ML: Machine Learning and Artificial Intelligence.
        DEVOPS: Development Operations and infrastructure.
        QA: Quality Assurance and testing.
        MOBILE: Mobile application development (iOS/Android).
        CLOUD: Cloud computing architecture and services.
        DATA: Data engineering and analysis.
        SECURITY: Cybersecurity and information protection.
    """

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


class FinancialQualification(Enum):
    """
    Professional certifications and qualifications for financial staff.

    Values:
        ACCA: Association of Chartered Certified Accountants.
        CIMA: Chartered Institute of Management Accountants.
        ACPM: Association of Certified Professional Managers.
        CPA: Certified Public Accountant.
        CIA: Certified Internal Auditor.
        CFA: Chartered Financial Analyst.
    """

    ACCA = "ACCA"
    CIMA = "CIMA"
    ACPM = "ACPM"
    CPA = "CPA"
    CIA = "CIA"
    CFA = "CFA"


class ITQualificationLevel(Enum):
    """
    Seniority levels for IT professionals.

    Values:
        JUNIOR: Entry-level professional (0-2 years experience).
        MIDDLE: Experienced professional (2-5 years experience).
        SENIOR: Expert professional (5+ years experience).
    """

    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
