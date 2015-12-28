# -*- coding: utf-8 -*-
# © 2015 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Connector CVA",
    "summary": "Module to sync with CVA web-services",
    "license": "AGPL-3",
    "version": "8.0.1.0.0",
    "author": "JARSA Sistemas, S.A. de C.V., Odoo Community Association (OCA)",
    "website": "http://www.jarsa.com.mx",
    "category": "connector",
    "depends": [
        'website_sale'
    ],
    "data": [
        'views/cva_config_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    "installable": False,
}
