# Copyright 2024 Onestein
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Hr Expense Fleet",
    "summary": "Allows to create expenses for fleet",
    "version": "16.0.1.0.0",
    "category": "Human Resources/Expenses",
    "website": "https://github.com/OCA/hr-expense",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["hr_expense", "hr_fleet", "product_analytic"],
    "data": [
        "data/hr_expense_data.xml",
        "views/fleet_vehicle_odometer_view.xml",
        "views/fleet_vehicle_view.xml",
        "views/hr_expense_view.xml",
        "views/product_view.xml",
    ],
}
