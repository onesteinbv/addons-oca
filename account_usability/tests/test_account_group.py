from odoo.tests.common import TransactionCase


class AccountGroupTest(TransactionCase):
    def test_group_accounts(self):
        group = self.env["account.group"].create(
            {
                "name": "Test Group",
                "code_prefix_start": "1000",
                "code_prefix_end": "1999",
            }
        )

        account = self.env["account.account"].create(
            {"code": "1001", "name": "Test Account"}
        )
        account_2 = self.env["account.account"].create(
            {"code": "2000", "name": "Test Account"}
        )

        self.assertIn(account.id, group.account_ids.ids)
        self.assertNotIn(account_2.id, group.account_ids.ids)

        account_3 = self.env["account.account"].create(
            {"code": "1002", "name": "Test Account 2"}
        )
        self.assertIn(account_3.id, group.account_ids.ids)
