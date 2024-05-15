# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class TierReview(models.Model):
    _inherit = "tier.review"

    location = fields.Char()
    designation = fields.Char()
