from odoo import api, models


class Account(models.Model):
    _inherit = "account.account"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.mapped("group_id").invalidate_recordset()
        return res
