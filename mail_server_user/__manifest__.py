# Copyright 2024 Onestein B.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Email Server For User",
    "summary": "Allows users to add their own outgoing mail server from the user preferences.",
    "version": "16.0.1.0.0",
    "category": "Social Network",
    "website": "https://github.com/OCA/social",
    "author": ("Onestein, " "Odoo Community Association (OCA)"),
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/res_users_view.xml",
    ],
}
