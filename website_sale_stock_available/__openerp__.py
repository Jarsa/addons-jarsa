# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Product Stock Available",
    "summary": "This module help you out if the product is in stock or not",
    "version": "9.0.1.0.0",
    "category": "Ecommerce",
    "website": "www.jarsa.com.mx",
    "author": "DRC Systems - Cooperation by Jarsa Sistemas S.A de C.V",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "description": "test",
    "depends": [
        "website_sale",
        "stock"
    ],
    "data": [
        "views/res_config_view.xml",
        "views/website_templates.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
