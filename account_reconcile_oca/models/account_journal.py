# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    reconcile_mode = fields.Selection(
        [("edit", "Edit Move"), ("keep", "Keep Suspense Accounts")],
        default="edit",
        required=True,
    )
    company_currency_id = fields.Many2one(related="company_id.currency_id")
    reconcile_aggregate = fields.Selection(
        [
            ("statement", "Statement"),
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
        ],
        string="Reconcile aggregation",
        help="Aggregation to use on reconcile view",
    )

    def get_rainbowman_message(self):
        self.ensure_one()
        if self.get_journal_dashboard_datas()["number_to_reconcile"] > 0:
            return False
        return _("Well done! Everything has been reconciled")

    def open_action(self):
        # open reconcile window for bank and cash journals
        if self.type in ("bank", "cash") and not self._context.get("action_name"):
            self.ensure_one()
            action = self.env["ir.actions.act_window"]._for_xml_id(
                "account_reconcile_oca.action_bank_statement_line_reconcile"
            )
            action["context"] = self._context.copy()
            action["context"].update(
                {
                    "default_journal_id": self.id,
                    "view_ref": "account_reconcile_oca.bank_statement_line_form_reconcile_view",
                    "search_view_ref": "account_statement_base.account_bank_statement_line_search",
                }
            )
            action["view_mode"] = "list,kanban"
            action["views"] = [
                (False, "list"),
                (
                    self.env.ref(
                        "account_reconcile_oca.bank_statement_line_reconcile_view"
                    ).id,
                    "kanban",
                ),
            ]
            return action
        return super().open_action()

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        """Populate all bank and cash journal's data dict with relevant information for the kanban card."""
        super()._fill_bank_cash_dashboard_data(dashboard_data)
        bank_cash_journals = self.filtered(
            lambda journal: journal.type in ("bank", "cash")
        )
        if not bank_cash_journals:
            return
        for journal in bank_cash_journals:
            dashboard_data[journal.id].update(
                {
                    "show_reconcile_button_with_no_entries_to_reconcile": journal.company_id.show_reconcile_button_with_no_entries_to_reconcile
                }
            )
