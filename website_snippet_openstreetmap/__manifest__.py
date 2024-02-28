# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Snippet OpenStreetMap",
    "category": "Website",
    "version": "16.0.1.0.1",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "depends": [
        "base_geolocalize",
        "website",
    ],
    "data": [
        "views/snippets/s_openstreetmap.xml",
        "views/snippets/snippets.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
    ],
    "assets": {
        "website.assets_wysiwyg": [
            "website_snippet_openstreetmap/static/src/snippets/s_openstreetmap/options.esm.js",
        ],
    },
}
