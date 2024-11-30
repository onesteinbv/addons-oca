# Copyright 2024 Onestein B.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestMailServerUser(TransactionCase):
    def setUp(self):
        super(TestMailServerUser, self).setUp()
        self.user1 = self.env["res.users"].create(
            {
                "login": "user1@somemail.com",
                "email": "user1@somemail.com",
                "partner_id": self.env["res.partner"].create({"name": "User 1"}).id,
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                        ],
                    )
                ],
            }
        )

    def test_setup_outgoing_mail_server(self):
        ir_mail_server_action = self.user1.setup_outgoing_mail_server()
        self.assertFalse(ir_mail_server_action["res_id"])
        self.assertEqual(
            ir_mail_server_action["context"]["default_from_filter"], self.user1.email
        )
        self.assertEqual(
            ir_mail_server_action["context"]["default_smtp_user"], self.user1.email
        )
        ir_mail_server_id = self.env["ir.mail_server"].create(
            {
                "name": "My Outgoing Mail Server",
                "smtp_host": "localhost",
                "smtp_user": "user1@somemail.com",
            }
        )
        ir_mail_server_action = self.user1.setup_outgoing_mail_server()
        self.assertEqual(ir_mail_server_action["res_id"], ir_mail_server_id.id)
        self.assertEqual(ir_mail_server_id.from_filter, self.user1.email)
