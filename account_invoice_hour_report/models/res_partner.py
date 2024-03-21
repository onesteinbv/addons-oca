# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    print_timesheet_employee = fields.Boolean(
        "Print Employee on Timesheet Report")
