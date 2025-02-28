# Copyright 2023 Domatix - Carlos Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    subscription_id = fields.Many2one(
        comodel_name="sale.subscription", string="Subscription"
    )
    subscription_start_date = fields.Date(readonly=True)
    subscription_end_date = fields.Date(readonly=True)

    def action_open_subscription(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "subscription_oca.sale_subscription_action"
        )
        action["domain"] = [("id", "=", self.subscription_id.id)]
        return action
