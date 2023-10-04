
from odoo import fields, models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    preview_attachment_id = fields.Many2one(
        string="Main Attachment",
        comodel_name='ir.attachment',
        related="move_id.message_main_attachment_id",
    )
