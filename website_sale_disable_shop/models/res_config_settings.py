# Copyright 2024 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    shop_enabled = fields.Boolean(related="website_id.shop_enabled", readonly=False)
