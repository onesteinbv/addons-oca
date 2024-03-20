# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_is_zero


class AccountReconcileAbstract(models.AbstractModel):
    _name = "account.reconcile.abstract"
    _description = "Account Reconcile Abstract"

    reconcile_data_info = fields.Serialized(
        compute="_compute_reconcile_data_info",
        prefetch=False,
    )
    company_id = fields.Many2one("res.company")
    add_account_move_line_id = fields.Many2one(
        "account.move.line",
        check_company=True,
        store=False,
        default=False,
        prefetch=False,
    )
    manual_reference = fields.Char(store=False, default=False, prefetch=False)
    manual_delete = fields.Boolean(
        store=False,
        default=False,
        prefetch=False,
    )
    currency_id = fields.Many2one("res.currency", readonly=True)
    foreign_currency_id = fields.Many2one("res.currency")
    company_currency_id = fields.Many2one(string="Company Currency",
        comodel_name="res.currency", related="company_id.currency_id"
    )

    def _get_reconcile_line(
        self, line, kind, is_counterpart=False, max_amount=False, from_unreconcile=False
    ):
        account_move_line_obj = self.env["account.move.line"]
        date = self.date if "date" in self._fields else line.date
        original_amount = amount = line.debit - line.credit
        if is_counterpart:
            amount = line.amount_residual_currency or line.amount_residual
            amount_currency = line.currency_id or self.company_id.currency_id
            original_amount = line.amount_residual
            if max_amount:
                currency_max_amount = self.company_id.currency_id._convert(
                    max_amount, amount_currency, self.company_id, date
                )
                if abs(amount) > abs(currency_max_amount):
                    amount = currency_max_amount
            amount = -amount
            original_amount = -original_amount
        else:
            amount_currency = line.currency_id
            amount = self.company_id.currency_id._convert(
                amount, amount_currency, self.company_id, date
            )
        currency_amount = amount
        amount = amount_currency._convert(
            amount, self.company_id.currency_id, self.company_id, date
        )
        vals = {
            "reference": "account.move.line;%s" % line.id,
            "id": line.id,
            "account_id": line.account_id.name_get()[0],
            "partner_id": line.partner_id and line.partner_id.name_get()[0] or False,
            "date": fields.Date.to_string(line.date),
            "name": line.name,
            "debit": amount if amount > 0 else 0.0,
            "credit": -amount if amount < 0 else 0.0,
            "amount": amount,
            "net_amount": 0,
            "currency_id": self.company_id.currency_id.id,
            "line_currency_id": line.currency_id.id,
            "currency_amount": currency_amount,
            "analytic_distribution": line.analytic_distribution,
            "kind": kind,
        }
        if from_unreconcile:
            vals.update(
                {
                    "id": False,
                    "counterpart_line_id": (
                        (
                            line.matched_debit_ids
                            and line.matched_debit_ids[0].mapped("debit_move_id")
                            or account_move_line_obj
                        )
                        | (
                            line.matched_credit_ids
                            and line.matched_credit_ids[0].mapped("credit_move_id")
                            or account_move_line_obj
                        )
                    ).id,
                }
            )
        if not float_is_zero(
            amount - original_amount, precision_digits=line.currency_id.decimal_places
        ):
            vals["original_amount"] = abs(original_amount)
            vals["original_amount_unsigned"] = original_amount
        if is_counterpart:
            vals["counterpart_line_id"] = line.id
        return vals
