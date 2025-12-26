from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def get_website_logo_url(self):
        website = self.get_current_website()
        logo_url = False
        if website:
            logo_url = f"url('/website/image/website/{website.id}/logo')"
            default_logo = website._default_logo()
            uses_default_logo = not website.logo or website.logo == default_logo
            if uses_default_logo:
                if not website.company_id.uses_default_logo:
                    logo_url = (
                        f"url('/website/image/res.company/"
                        f"{website.company_id.id}/logo')"
                    )
        return logo_url
