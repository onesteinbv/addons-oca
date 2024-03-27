# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    is_non_billable = fields.Boolean(
        string="Non Billable",
        help="Checking this would mark this timesheet entry as Non Billable",
    )

    @api.constrains("is_non_billable")
    def _constrains_is_non_billable(self):
        for line in self:
            if (
                line.timesheet_invoice_id
                and line.so_line.product_id.invoice_policy == "delivery"
            ):
                raise ValidationError(
                    _(
                        "You can not modify timesheets in a way that would affect "
                        "invoices since these timesheets were already invoiced."
                    )
                )

    @api.depends("is_non_billable")
    def _compute_timesheet_invoice_type(self):
        res = super()._compute_timesheet_invoice_type()
        for line in self:
            if line.is_non_billable:
                line.timesheet_invoice_type = "non_billable"
        return res
