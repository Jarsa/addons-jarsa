# -*- coding: utf-8 -*-
# © 2015 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale order report ticket",
    "summary": "Creates sale order report for thermal printers",
    "version": "8.0.1.0.0",
    "category": "sale",
    "website": "https://www.jarsa.com.mx/",
    "author": "Jarsa Sistemas, S.A. de C.V., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": [
        "sale",
    ],
    "data": [
        'report/report_sale_order_ticket.xml'
    ],
}
