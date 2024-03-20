# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.depends("date")
    def _compute_week_number(self):
        for line in self:
            week_number = line.date.isocalendar()
            line.week_number = "W%s %s" % (str(week_number[1]), (str(week_number[0])))

    is_approved = fields.Boolean()
    project_user_id = fields.Many2one(
        "res.users", related="project_id.user_id", store=True)
    week_number = fields.Char(compute="_compute_week_number", store=True)

    def action_unapprove(self):
        if self.filtered(lambda x: x.timesheet_invoice_id):
            raise ValidationError(
                _("You cannot unapprove a timesheet line already invoiced"))
        self.write({"is_approved": False})
