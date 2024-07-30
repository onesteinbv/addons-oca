# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_reconcile_button_with_no_entries_to_reconcile = fields.Boolean(
        related="company_id.show_reconcile_button_with_no_entries_to_reconcile",
        readonly=False,
    )
