# Copyright 2024 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Agreement Legal Tier Validation Sign",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "category": "Contract",
    "author": "Onestein",
    "website": "https://www.onestein.nl",
    "depends": [
        "base_tier_validation_sign",
        "agreement_tier_validation",
    ],
    "data": ["report/agreement.xml", "wizard/comment_wizard_view.xml"],
    "auto_install": True,
}
