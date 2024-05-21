# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"

    requires_signature = fields.Boolean(compute="_compute_requires_signature")
    next_review = fields.Char(compute="_compute_next_review")

    def _compute_requires_signature(self):
        for rec in self:
            requires_signature = rec.review_ids.filtered(
                lambda r: r.status == "pending" and (self.env.user in r.reviewer_ids)
            ).mapped("requires_signature")
            rec.requires_signature = True in requires_signature

    def _add_comment(self, validate_reject, reviews):
        res = super()._add_comment(validate_reject=validate_reject, reviews=reviews)
        if self.requires_signature and validate_reject == "validate":
            res["context"].update({"default_requires_signature": True})
        return res
