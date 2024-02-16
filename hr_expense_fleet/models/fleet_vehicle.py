# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    product_id = fields.Many2one(
        "product.product",
        string="Expense Category",
        domain="[('can_be_expensed', '=', True),('can_be_used_for_fleet', '=', True)]",
        help="Defines default expense category for this vehicle's trips",
    )
