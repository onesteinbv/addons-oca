# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers.portal import PaymentPortal


class Payment(PaymentPortal):
    @http.route(
        "/crowdfunding/<model('crowdfunding.challenge'):challenge>/pay",
        type="http",
        methods=["GET"],
        auth="user",
        website=True,
        sitemap=False,
    )
    def crowdfunding_pay(self, challenge, amount):
        kwargs = dict(
            amount=self._cast_as_float(amount),
            partner_id=request.env.user.partner_id.id,
            currency_id=challenge.company_id.currency_id.id,
            crowdfunding_challenge_id=challenge.id,
        )
        kwargs["access_token"] = payment_utils.generate_access_token(
            kwargs["partner_id"], kwargs["amount"], kwargs["currency_id"]
        )
        return self.payment_pay(**kwargs)

    def _get_extra_payment_form_values(self, crowdfunding_challenge_id=None, **kwargs):
        values = super()._get_extra_payment_form_values(**kwargs)
        if crowdfunding_challenge_id:
            values["transaction_route"] = (
                f"/crowdfunding/{crowdfunding_challenge_id}/transaction"
            )
        return values

    @http.route(
        "/crowdfunding/<model('crowdfunding.challenge'):challenge>/transaction",
        type="json",
        auth="public",
    )
    def crowdfunding_transaction(self, challenge, amount, access_token, **kwargs):
        amount = self._cast_as_float(amount)
        partner_id = request.env.user.partner_id.id
        currency_id = challenge.company_id.currency_id.id

        if not payment_utils.check_access_token(
            access_token, partner_id, amount, currency_id
        ):
            raise ValidationError(_("The access token is invalid."))

        self._validate_transaction_kwargs(kwargs)
        transaction = self._create_transaction(
            amount=amount, currency_id=currency_id, partner_id=partner_id, **kwargs
        )
        transaction.crowdfunding_challenge_id = challenge
        self._update_landing_route(transaction, access_token)
        return transaction._get_processing_values()
