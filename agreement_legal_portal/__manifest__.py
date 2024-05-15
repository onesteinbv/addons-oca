# Copyright 2024 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Agreement Legal Portal",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "category": "Contract",
    "author": "Onestein",
    "website": "https://www.onestein.nl",
    "depends": [
        "portal",
        "agreement_legal",
    ],
    "data": [
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "templates/agreement_portal_templates.xml",
        "views/agreement_view.xml",
    ],
}