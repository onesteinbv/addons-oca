# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.delivery import Delivery

_logger = logging.getLogger(__name__)


class WebsiteSaleSendcloudDelivery(Delivery):
    def _order_summary_values(self, order, **post):
        res = super()._order_summary_values(order, **post)
        if order.carrier_id.delivery_type == "sendcloud":
            res.update({"sendcloud_details": order.sendcloud_details})
        return res

    @http.route(
        ["/shop/sendcloud_update_service_point_address"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def sendcloud_update_service_point_address(self, **post):
        if post.get("order_id"):
            order = request.env["sale.order"].sudo().browse(post.get("order_id"))
            order.write(
                {
                    "sendcloud_service_point_address": post.get(
                        "sendcloud_service_point_address"
                    )
                }
            )
        return True
