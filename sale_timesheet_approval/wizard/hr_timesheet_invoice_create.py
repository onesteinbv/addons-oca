# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrTimesheetInvoiceCreate(models.TransientModel):
    _name = 'hr.timesheet.invoice.create'
    _description = 'Create invoice from timesheet'

    def do_approve(self):
        self.ensure_one()
        line_ids = self.env.context.get('active_ids')
        lines = self.env['account.analytic.line'].browse(
            line_ids).filtered(lambda x: not x.is_approved)
        lines.write({'is_approved': True})

    def do_create(self):
        self.ensure_one()
        ctx, payment = self._do_create()
        return payment.with_context(ctx).create_invoices()

    def _do_create(self):
        line_ids = self.env.context.get('active_ids')
        lines = self.env['account.analytic.line'].browse(line_ids)
        sale_orders = lines.mapped('so_line.order_id')
        ctx = {
            "active_model": 'sale.order',
            "active_ids": sale_orders.ids,
            'open_invoices': True,
        }
        payment = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'delivered',
        })
        lines.filtered(lambda x: not x.is_approved).write({
            'is_approved': True
        })
        return ctx, payment
