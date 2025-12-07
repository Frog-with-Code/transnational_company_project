Multi-modular transnational company program
===========================================


Transnational company is a modular Python project that models the core subsystems of a large
international company: HR, finance, logistics, common utilities, and company structure. It 
provides rich domain objects and services for employees, budgeting and transactions, transport 
and cargo management, warehouses, locations, and products, all covered by an extensive pytest 
test suite. The package is designed as clean, testable business logic that can serve as a backend
foundation or a teaching example for domain-driven design in Python.

.. toctree::
   :maxdepth: 5
   :caption: Content:

Company structure
-----------------
.. automodule:: company.company_structure.companies
   :members:

Finance
-------
.. automodule:: company.finance.budget_management
   :members:

.. automodule:: company.finance.budget
   :members:

.. automodule:: company.finance.transaction
   :members:

HR
--
.. automodule:: company.hr.employees
   :members:
.. automodule:: company.hr.employee_manager
   :members:

Logistics
---------
.. automodule:: company.logistics.transport
   :members:

.. automodule:: company.logistics.warehouse
   :members: