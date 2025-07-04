# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slug


class CrowdfundingChallenge(models.Model):
    _name = "crowdfunding.challenge"
    _description = "Crowdfunding challenge"
    _inherit = ["mail.thread", "website.published.mixin"]
    _mail_post_access = "read"
    _mail_flat_thread = False

    name = fields.Char(required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("claimed", "Claimed"),
            ("submitted", "Submitted"),
            ("done", "Done"),
        ],
        default="draft",
    )
    description = fields.Html()
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(related="company_id.currency_id")
    claimed_partner_id = fields.Many2one("res.partner", string="Claimed by partner")
    transaction_count = fields.Integer(compute="_compute_transactions", store=True)
    transaction_ids = fields.One2many(
        "payment.transaction", "crowdfunding_challenge_id"
    )
    pledged_amount = fields.Monetary(
        compute="_compute_transactions", readonly=True, store=True
    )

    @api.depends("transaction_ids.amount", "transaction_ids.state")
    def _compute_transactions(self):
        for this in self:
            this.transaction_count = len(this.transaction_ids)
            this.pledged_amount = sum(
                this.transaction_ids.filtered(lambda x: x.state == "done").mapped(
                    "amount"
                )
            )

    def _compute_website_url(self):
        for this in self:
            this.website_url = f"/crowdfunding/{slug(this)}"

    def action_cancel(self):
        self.write(
            {"state": "draft", "website_published": False, "claimed_partner_id": False}
        )

    def action_open(self):
        self.filtered(lambda x: x.state == "draft").write(
            {"state": "open", "website_published": True}
        )

    def action_payment_transactions(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "payment.action_payment_transaction"
        )
        return dict(action, domain=[("crowdfunding_challenge_id", "in", self.ids)])

    def _claim(self, partner):
        self.filtered(lambda x: x.state == "open").write(
            {
                "claimed_partner_id": partner.id,
                "state": "claimed",
            }
        )

    def _can_claim(self, partner):
        self.ensure_one()
        return not self.claimed_partner_id and self.state == "open"
