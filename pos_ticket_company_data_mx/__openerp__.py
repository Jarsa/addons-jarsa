# coding: utf-8` or `# -*- coding: utf-8 -*-

{
    "name": "Point of Sale Ticket Company data MX",
    "version": "8.0.0.1.0",
    "category": "Point of Sale",
    "author": "Jarsa Sistemas, S.A. de C.V., Odoo Community Association (OCA)",
    "website": "www.jarsa.com.mx",
    "depends": [
        'point_of_sale',
        'l10n_mx_partner_address',
        ],
    "summary": "Add address and VAT fields to POS ticket",
    "license": "AGPL-3",
    "data": [
        'views/pos_ticket_company_data.xml'
    ],
    "qweb": [
        'static/src/xml/pos.xml',
    ],
    "application": True,
    "installable": False,
}
