# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

import werkzeug

from odoo import http
from odoo.http import request


class CrowdfundingController(http.Controller):
    @http.route(["/crowdfunding"], type="http", auth="public", website=True)
    def list(self):
        values = self._list_render_context()
        return request.render("crowdfunding.template_challenge_list", values)

    def _list_render_context(self):
        return {
            "results": request.env["crowdfunding.challenge"].search(
                [("is_published", "=", True)]
            ),
        }

    @http.route(
        ["/crowdfunding/<model('crowdfunding.challenge'):challenge>"],
        type="http",
        auth="public",
        website=True,
    )
    def detail(self, challenge):
        values = self._detail_render_context(challenge)
        return request.render("crowdfunding.template_challenge_detail", values)

    def _detail_render_context(self, challenge, **kwargs):
        return {
            "object": challenge,
        }

    @http.route(
        ["/crowdfunding/<model('crowdfunding.challenge'):challenge>/claim"],
        type="http",
        auth="user",
        website=True,
    )
    def claim(self, challenge):
        if request.env.user.is_public:
            return request.redirect(
                f"/web/login?redirect=/crowdfunding/{challenge.id}/claim"
            )
        if challenge._can_claim(request.env.user.partner_id):
            challenge.sudo()._claim(request.env.user.partner_id)
            values = self._detail_render_context(challenge)
            return request.render("crowdfunding.template_challenge_detail", values)
        else:
            # TODO nicer error
            raise werkzeug.exceptions.NotFound()
