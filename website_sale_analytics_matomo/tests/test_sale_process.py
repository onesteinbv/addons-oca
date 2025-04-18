# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale_analytics_matomo.controllers.main import WebsiteSaleMatomo


@tagged("post_install", "-at_install")
class TestWebsiteSaleMatomo(HttpCaseWithUserDemo):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.WebsiteSaleController = WebsiteSaleMatomo()

        # make sure the configuration for Google Analytics is disabled
        cls.website.write(
            {
                "google_analytics_key": False,
            }
        )
        # enable Matomo Analytics
        cls.website.write(
            {
                "has_matomo_analytics": True,
                "matomo_analytics_host": "https://example.matomo.org",
                "matomo_analytics_id": "M-XXXXXXXXXXX",
            }
        )

    def test_01_matomo_tours_analytics(self):
        """get_combination_info is adapted for Matomo Analytics"""
        # Re-use the same tour defined for Google Analytics
        # Data for google_analytics_view_item
        attribute = self.env["product.attribute"].create(
            {
                "name": "Color",
                "sequence": 10,
                "display_type": "color",
                "value_ids": [
                    Command.create(
                        {
                            "name": "Red",
                        }
                    ),
                    Command.create(
                        {
                            "name": "Pink",
                        }
                    ),
                ],
            }
        )
        self.env["product.template"].create(
            {
                "name": "Colored T-Shirt",
                "standard_price": 500,
                "list_price": 750,
                "detailed_type": "consu",
                "website_published": True,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attribute.id,
                            "value_ids": attribute.value_ids,
                        }
                    )
                ],
            }
        )
        self.start_tour("/shop", "google_analytics_view_item")
        # Data for google_analytics_add_to_cart
        self.env["product.template"].create(
            {
                "name": "Basic Shirt",
                "standard_price": 500,
                "detailed_type": "consu",
                "website_published": True,
            }
        )
        self.start_tour("/shop", "google_analytics_add_to_cart")

    def test_02_matomo_order_tracking_info(self):
        """Check the order tracking info at the confirmation page."""
        product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "sale_ok": True,
                "website_published": True,
                "lst_price": 3000.0,
            }
        )

        with MockRequest(self.env, website=self.website):
            # Add product to cart
            self.WebsiteSaleController.cart_update_json(
                product_id=product.id, add_qty=1
            )

            # Check shop payment confirmation values
            sale_order = self.website.sale_get_order()
            res_dict = (
                self.WebsiteSaleController._prepare_shop_payment_confirmation_values(
                    sale_order
                )
            )
            order_tracking_info = res_dict["order_tracking_info"]
            self.assertEqual(order_tracking_info["order_name"], sale_order.name)
            self.assertEqual(order_tracking_info["subtotal"], sale_order.amount_untaxed)
