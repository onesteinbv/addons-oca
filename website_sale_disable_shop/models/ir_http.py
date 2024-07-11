# Copyright 2024 Onestein
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from pathlib import Path

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls, endpoint):
        res = cls._check_shop_enabled_disabled()
        if res:
            return res
        return super()._dispatch(endpoint)

    @classmethod
    def _serve_fallback(cls):
        res = cls._check_shop_enabled_disabled()
        if res:
            return res
        return super()._serve_fallback()

    @classmethod
    def _check_shop_enabled_disabled(cls):
        # if not website request - skip
        website = request.env["website"].sudo().get_current_website()
        if not website:
            return None
        if not website.shop_enabled:
            path = request.httprequest.path
            if path == "/shop" or Path("/shop") in Path(path).parents:
                if path == "/shop/cart" and request.params.get("type") == "popover":
                    return None
                return request.redirect("/")
