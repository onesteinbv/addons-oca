# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    show_reconcile_button_with_no_entries_to_reconcile = fields.Boolean(
        string="Show Reconcile Button Even If There Are No Entries to reconcile",
        default=False,
    )
