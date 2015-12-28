# coding: utf-8` or `# -*- coding: utf-8 -*-

{
    "name": "POS Order Report",
    "version": "8.0.0.1.0",
    "category": "Point of Sale",
    "author": "Jarsa Sistemas, S.A. de C.V., Odoo Community Association (OCA)",
    "website": "www.jarsa.com.mx",
    "depends": [
        "point_of_sale",
        ],
    "summary": "Calculates all the week and montly sales",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "pandas",
        ],
    },
    "data": [
        "reports/pos_order_by_date_report.xml",
        "wizard/pos_order_wizard_view.xml",
    ],
    "application": True,
    "installable": False,
}
