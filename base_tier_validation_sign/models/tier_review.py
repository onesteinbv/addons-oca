# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class TierReview(models.Model):
    _inherit = "tier.review"

    signature = fields.Image(help="Signature",attachment=True)
    requires_signature = fields.Boolean(related="definition_id.requires_signature", readonly=True)
