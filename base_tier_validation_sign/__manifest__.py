# Copyright 2024 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Tier Validation Sign",
    "summary": "Extends the functionality of base"
    "tier validation process to add signatures",
    "version": "16.0.1.0.0",
    "category": "Contract Management",
    "website": "https://github.com/OCA/server-ux",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base_tier_validation"],
    "data": ["view/tier_definition_view.xml", "wizard/comment_wizard_view.xml"],
}
