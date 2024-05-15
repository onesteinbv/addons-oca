import binascii

from odoo import _, fields, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class PortalAgreement(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if "agreement_count" in counters:
            agreement_model = request.env["agreement"]
            agreement_count = (
                agreement_model.search_count(self._get_filter_domain(partner))
                if agreement_model.check_access_rights("read", raise_exception=False)
                else 0
            )
            values["agreement_count"] = agreement_count
        return values

    def _agreement_get_page_view_values(self, agreement, access_token, **kwargs):
        values = {
            "page_name": "agreements",
            "agreement": agreement,
        }
        return self._get_page_view_values(
            agreement,
            access_token,
            values,
            "my_agreements_history",
            False,
            **kwargs
        )

    def _get_filter_domain(self, partner):
        return [
            ("is_template", "=", False)
        ]

    @http.route(
        ["/my/agreements", "/my/agreements/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_agreements(
            self, page=1, date_begin=None, date_end=None, sortby=None
    ):
        values = self._prepare_portal_layout_values()
        agreement_obj = request.env["agreement"]
        # Avoid error if the user does not have access.
        if not agreement_obj.check_access_rights("read", raise_exception=False):
            return request.redirect("/my")
        partner = request.env.user.partner_id
        domain = self._get_filter_domain(partner)
        searchbar_sortings = {
            "date": {"label": _("Date"), "order": "start_date desc"},
            "name": {"label": _("Name"), "order": "name desc"},
            "code": {"label": _("Reference"), "order": "code desc"},
        }
        # default sort by order
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # count for pager
        agreement_count = agreement_obj.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/agreements",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
            },
            total=agreement_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        agreements = agreement_obj.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_agreements_history"] = agreements.ids[:100]
        values.update(
            {
                "date": date_begin,
                "agreements": agreements,
                "page_name": "agreements",
                "pager": pager,
                "default_url": "/my/agreements",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("agreement_legal_portal.portal_my_agreements", values)

    @http.route(
        ["/my/agreements/<int:agreement_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_agreement_detail(
            self, agreement_id, access_token=None, report_type=None, download=False, message=False, **kw
    ):
        try:
            agreement_sudo = self._document_check_access(
                "agreement", agreement_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        if report_type in ("html", "pdf", "text"):
            return self._show_report(model=agreement_sudo, report_type=report_type,
                                     report_ref="agreement_legal.partner_agreement_contract_document",
                                     download=download)

        values = self._agreement_get_page_view_values(
            agreement_sudo, access_token, **kw
        )
        values.update({
            "message": message,
            "report_type": "html",
        })
        return request.render("agreement_legal_portal.portal_agreement_page", values)

    @http.route(
        ["/my/agreements/<int:agreement_id>/accept"],
        type="json",
        auth="public",
        website=True,
        csrf=False
    )
    def portal_my_agreement_accept(
            self, agreement_id, access_token=None, name=None, signature=None):
        access_token = access_token or request.httprequest.args.get("access_token")
        try:
            agreement_sudo = self._document_check_access(
                "agreement", agreement_id, access_token
            )
        except (AccessError, MissingError):
            return {"error": _("Invalid order.")}

        if agreement_sudo.signature:
            return {"error": _("The agreement is already signed.")}
        if not signature:
            return {"error": _("Signature is missing.")}
        partner_id = None
        if not request.env.user._is_public():
            partner_id = request.env.user.partner_id.id
        if not partner_id:
            partner_id = agreement_sudo.partner_contact_id
        if not partner_id:
            partner_id = request.env["res.partner"].search([("name", "=ilike", name)], limit=1)
        try:
            agreement_sudo.write({
                "partner_signed_user_id": partner_id,
                "partner_signed_date": fields.Datetime.now(),
                "signature": signature
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error):
            return {"error": _("Invalid signature data.")}

        pdf = \
        request.env["ir.actions.report"].sudo()._render_qweb_pdf("agreement_legal.partner_agreement_contract_document",
                                                                 [agreement_sudo.id])[
            0]

        agreement_sudo.write({"signed_contract": pdf, "signed_contract_filename": "%s.pdf" % agreement_sudo.name})

        _message_post_helper(
            "agreement",
            agreement_sudo.id,
            _("Agreement signed by %s", name),
            attachments=[("%s.pdf" % agreement_sudo.name, pdf)],
            token=access_token,
        )

        query_string = "&message=sign_ok"
        return {
            "force_refresh": True,
            "redirect_url": agreement_sudo.get_portal_url(query_string=query_string),
        }
