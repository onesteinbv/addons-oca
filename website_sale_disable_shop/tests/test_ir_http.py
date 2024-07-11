from odoo.tests import HttpCase


class TestIrHttp(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].sudo().get_current_website()
        self.path = "/shop"

    def test_dispatch_shop_enabled(self):
        # Test that a user can access "/shop
        response = self.url_open(self.path)
        self.assertEqual(
            response.status_code,
            200,
            "Expected the response status code to be 200 which means no redirection",
        )

    def test_dispatch__shop_disabled(self):
        # Test that a user cannot access "/shop
        self.website.shop_enabled = False
        response = self.url_open(self.path, allow_redirects=False)
        self.assertEqual(
            response.status_code,
            303,
            "Expected the response status code to be 303 indicating a redirect",
        )
