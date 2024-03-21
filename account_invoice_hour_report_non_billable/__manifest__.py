# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Invoice Hour Report With Non Billable Timesheets',
    "version": "16.0.1.0.0",
    'author': 'Onestein',
    'category': 'Accounting & Finance',
    'website': 'https://www.onestein.eu',
    'depends': [
        'account_invoice_hour_report','sale_timesheet_line_non_billable'
    ],
    'data': [
        'templates/hour_report_template.xml',
    ],
    'installable': True,
    'auto_install': True,
}
