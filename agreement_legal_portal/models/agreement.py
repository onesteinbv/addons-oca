from odoo import _, fields, models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = [
        "agreement",
        "portal.mixin",
    ]

    signature = fields.Image(
        string="Signature",
        copy=False, attachment=True, max_width=1024, max_height=1024)

    def _compute_access_url(self):
        for record in self:
            record.access_url = "/my/agreements/{}".format(record.id)

    def _get_report_base_filename(self):
        self.ensure_one()
        return "%s" % self.name

    def action_agreement_send(self):
        self.ensure_one()
        template = self.env.ref(
            "agreement_legal_portal.agreement_email_template", False
        )
        compose_form = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = dict(
            default_model="agreement",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

