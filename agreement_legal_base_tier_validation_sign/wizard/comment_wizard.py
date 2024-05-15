# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CommentWizard(models.TransientModel):
    _inherit = "comment.wizard"

    location = fields.Char()
    designation = fields.Char()

    @api.model
    def default_get(self, fields):
        res = super(CommentWizard, self).default_get(fields)
        res.update({
            "location": self.env.user.city or (self.env.user.country_id and self.env.user.country_id.name) or "",
            "designation": self.env.user.function
        })
        return res

    def add_comment(self):
        if self.validate_reject == "validate":
            self.review_ids.filtered(
                lambda r: r.status == "pending" and (self.env.user in r.reviewer_ids)
            ).write({"location": self.location, "designation": self.designation})
        return super().add_comment()
