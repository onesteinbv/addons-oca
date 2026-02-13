# Copyright 2026 Anjeel Haria
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    breadcrumb_enabled = fields.Boolean(
        string="Show Breadcrumbs",
        related="website_id.breadcrumb_enabled",
        readonly=False,
    )
