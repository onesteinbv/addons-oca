# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CommentWizard(models.TransientModel):
    _inherit = "comment.wizard"

    signature = fields.Image(help="Signature")
    partner_name = fields.Char()
    requires_signature = fields.Boolean()

    @api.model
    def default_get(self, fields):
        res = super(CommentWizard, self).default_get(fields)
        res.update({"partner_name": self.env.user.partner_id.name})
        return res

    def add_comment(self):
        if self.validate_reject == "validate":
            self.review_ids.filtered(
                lambda r: r.status == "pending" and (self.env.user in r.reviewer_ids)
            ).write({"signature": self.signature})
        return super().add_comment()
