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

    def get_rainbowman_message(self):
        self.ensure_one()
        if self.get_journal_dashboard_datas()["number_to_reconcile"] > 0:
            return False
        return _("Well done! Everything has been reconciled")

    def open_action(self):
        # opem reconcile window for bank and cash journals
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
