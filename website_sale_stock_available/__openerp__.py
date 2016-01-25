# -*- coding: utf-8 -*-
# © <2016> <DRC Systems - ported by Jarsa Sistemas S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Product Stock Available",
    "summary": "Display if product is on stock in website",
    "version": "9.0.1.0.0",
    "category": "Ecommerce",
    "website": "http://www.jarsa.com.mx",
    "author": "DRC Systems & Jarsa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
        "stock",
    ],
    'data': [
        'views/res_config_view.xml',
        'views/website_templates.xml',
        'security/ir.model.access.csv',
    ],
}
