# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Payment Conekta Oxxo",
    "summary": "Payment Acquirer: Conekta Implementation",
    "version": "9.0.1.0.0",
    "category": "Hidden",
    "website": "https://www.jarsa.com.mx/",
    "author": "JARSA Sistemas, S.A. de C.V.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": ["conekta"],
    },
    "depends": [
        "payment_conekta",
        "webhook",
    ],
    "data": [
        "views/oxxo.xml",
        "data/webhook_data.xml",
        "views/assets_frontend.xml",
        "data/payment_acquirer_data.xml",
        "views/sale_order_report_view.xml",
    ],
    "demo": [
        "demo/payment_acquirer_demo.xml",
    ]
}
