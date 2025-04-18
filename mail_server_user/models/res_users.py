# Copyright 2024 Onestein B.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def setup_outgoing_mail_server(self):
        self.ensure_one()
        ir_mail_server_id = self.env["ir.mail_server"].search([], limit=1)
        if ir_mail_server_id and self.email:
            # Make sure that from_filter and smtp_user is set to user's email
            ir_mail_server_id.write(
                {"from_filter": self.email, "smtp_user": self.email}
            )
        return {
            "type": "ir.actions.act_window",
            "res_model": "ir.mail_server",
            "name": "Setup Outgoing Mail Server",
            "target": "new",
            "views": [(False, "form")],
            "res_id": ir_mail_server_id.id,
            "context": {
                "default_from_filter": self.email,
                "default_smtp_user": self.email,
            },
        }
