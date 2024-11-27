# Copyright 2024 Onestein B.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    ir_mail_server_id = fields.Many2one(
        "ir.mail_server",
        "Outgoing Email Server",
        help="The email server with least Priority would be used.Make sure the From filtering is set to your email",
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["ir_mail_server_id"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["ir_mail_server_id"]
