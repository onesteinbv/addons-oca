from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('analytic_line_ids.is_non_billable')
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()

    def _timesheet_compute_delivered_quantity_domain(self):
        """ Non billable timesheets should not be considered """
        domain = super(SaleOrderLine, self)._timesheet_compute_delivered_quantity_domain()
        domain += [('is_non_billable', '=', False)]
        return domain