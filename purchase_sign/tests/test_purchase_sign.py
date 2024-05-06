# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserPortal


@tagged("post_install", "-at_install")
class TestPurchaseSign(HttpCaseWithUserPortal):
    def test_01_portal_purchase_signature_tour(self):
        """The goal of this test is to make sure the portal user can sign PO."""
        self.user_portal.company_id.purchase_portal_confirmation_sign = True
        portal_user_partner = self.partner_portal
        # create a PO to be signed
        purchase_order = self.env["purchase.order"].create(
            {
                "name": "test PO",
                "partner_id": portal_user_partner.id,
                "state": "sent",
            }
        )
        self.env["purchase.order.line"].create(
            {
                "order_id": purchase_order.id,
                "product_id": self.env["product.product"]
                .create({"name": "A product"})
                .id,
            }
        )

        # must be sent to the user so he can see it
        email_act = purchase_order.action_rfq_send()
        email_ctx = email_act.get("context", {})
        purchase_order.with_context(**email_ctx).message_post_with_template(
            email_ctx.get("default_template_id")
        )

        self.start_tour("/", "purchase_signature", login="portal")

    def test_02_purchase_has_to_be_signed(self):
        """The goal of this test is to check whether PO needs signature if Online signature is turned off for the company."""
        self.user_portal.company_id.purchase_portal_confirmation_sign = False
        portal_user_partner = self.partner_portal
        purchase_order = self.env["purchase.order"].create(
            {
                "name": "test PO",
                "partner_id": portal_user_partner.id,
                "state": "sent",
            }
        )
        self.env["purchase.order.line"].create(
            {
                "order_id": purchase_order.id,
                "product_id": self.env["product.product"]
                .create({"name": "A product"})
                .id,
            }
        )
        self.assertFalse(purchase_order._has_to_be_signed())
