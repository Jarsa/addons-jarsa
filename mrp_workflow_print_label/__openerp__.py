# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Workflow Print Label",
    "summary": "Print MRP Workflow Label after Production",
    "version": "8.0.1.0.0",
    "category": "Manufacture",
    "website": "https://www.jarsa.com.mx/",
    "author": "JARSA Sistemas, S.A. de C.V.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mrp"
    ],
    "data": [
        'wizard/mrp_print_label.xml',
        'wizard/mrp_print_label_validate.xml',
        'views/mrp_production_view.xml',
        'views/mrp_print_reason_view.xml',
        'views/res_users_view.xml',
        'views/mrp_bom_view.xml',
        'reports/label.xml',
        "security/security.xml",
        "security/ir.model.access.csv",
    ],
}
