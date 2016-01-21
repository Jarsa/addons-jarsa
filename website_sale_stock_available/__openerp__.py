# -*- coding: utf-8 -*-

{
    'name': 'Website Sale Product Stock Available',
    'version': '9.0.1.0.0',
    'category': 'Ecommerce',
    'description': """
                    This module dispaly product stock in website product page
                    """,
    'author': 'DRC Systems - refactorized by Jarsa Sistemas S.A. de C.V.',
    'depends': ['website_sale', 'stock'],
    'data': [
        'views/res_config_view.xml',
        'views/website_templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
