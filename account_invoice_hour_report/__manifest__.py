# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Invoice hour report addition',
    "version": "16.0.1.0.0",
    'author': 'Onestein',
    'category': 'Accounting & Finance',
    'website': 'https://www.onestein.eu',
    'depends': [
        'sale_timesheet_approval',
    ],
    'data': [
        # 'data/report_paperformat.xml',
        # 'templates/layout.xml',
        'templates/hour_report_template.xml',
        # 'templates/hour_to_be_invoiced_report_template.xml',
        'views/hours_report.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
}
