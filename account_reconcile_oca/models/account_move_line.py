from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    paid_amount = fields.Monetary(
        compute="_compute_paid_amount",
        currency_field="company_currency_id",
    )

    def _compute_paid_amount(self):
        account_bank_statement_line_obj = self.env["account.bank.statement.line"]
        for rec in self:
            paid_amount = 0.0
            st_line = account_bank_statement_line_obj.browse(
                self._context.get("bank_statement_line_id")
            )
            if st_line.is_reconciled:
                (
                    _liquidity_lines,
                    suspense_lines,
                    _other_lines,
                ) = st_line._seek_for_lines()
                if _other_lines:
                    paid_amount += sum(
                        _other_lines.mapped("matched_debit_ids")
                        .filtered(lambda mdi: mdi.debit_move_id == rec)
                        .mapped("amount")
                    )
                    paid_amount += sum(
                        _other_lines.mapped("matched_credit_ids")
                        .filtered(lambda mdi: mdi.credit_move_id == rec)
                        .mapped("amount")
                    )
            rec.paid_amount = paid_amount

    def action_open_business_doc(self):
        res = super().action_open_business_doc()
        if self._context.get("open_in_new_window"):
            res["target"] = "new"
        return res
