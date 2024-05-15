from odoo.addons.agreement_legal_portal.controllers.main import PortalAgreement


class PortalAgreement(PortalAgreement):

    def _get_filter_domain(self, partner):
        res = super()._get_filter_domain(partner=partner)
        res.append(("state", "=", "active"))
        return res
