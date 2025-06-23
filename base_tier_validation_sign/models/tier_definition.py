# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class TierDefinition(models.Model):
    _inherit = "tier.definition"

    requires_signature = fields.Boolean(
        string="Requires Signature For Validation", default=False
    )
