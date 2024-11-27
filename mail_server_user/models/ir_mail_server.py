# Copyright 2024 Onestein B.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    smtp_user = fields.Char(groups="base.group_system,base.group_user")
    smtp_pass = fields.Char(groups="base.group_system,base.group_user")
    smtp_ssl_certificate = fields.Binary(groups="base.group_system,base.group_user")
    smtp_ssl_private_key = fields.Binary(groups="base.group_system,base.group_user")
