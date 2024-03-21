# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales Timesheet: Mark Timesheet Line As Non Billable",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/timesheet",
    "author": "Onestein, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "summary": "Mark Timesheet Line As Non Billable",
    "depends": ["sale_timesheet"],
    "data": ["views/account_analytic_line.xml", "views/project_task.xml", "report/report_timesheet_templates.xml"],
}
