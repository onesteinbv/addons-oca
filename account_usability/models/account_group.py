# Copyright 2018 FOREST AND BIOMASS ROMANIA SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import Command, api, fields, models


class AccountGroup(models.Model):
    _inherit = "account.group"

    account_ids = fields.One2many(
        comodel_name="account.account",
        compute="_compute_account_ids",
        string="Accounts",
    )

    @api.depends_context("company")
    @api.depends("code_prefix_start", "code_prefix_end")
    def _compute_account_ids(self):
        query = """
            SELECT
                a.id, g.id
            FROM
                account_account a
            JOIN
                account_group g
                ON g.code_prefix_start <= LEFT(
                    (a.code_store::json ->> %(company_id)s),
                    char_length(g.code_prefix_start)
                )
                AND g.code_prefix_end >= LEFT(
                    (a.code_store::json ->> %(company_id)s),
                    char_length(g.code_prefix_end)
                )
                AND g.company_id = %(company_id)s
            WHERE g.id IN %(group_ids)s
        """
        self.env.cr.execute(
            query,
            {
                "group_ids": tuple(self.ids),
                "company_id": str(self.env.company.root_id.id),
            },
        )
        res = self.env.cr.fetchall()
        group_accounts = defaultdict(list)
        for account_id, group_id in res:
            group_accounts[group_id].append(account_id)

        for group in self:
            group.account_ids = [Command.set(group_accounts[group.id])]
