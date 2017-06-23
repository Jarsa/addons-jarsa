# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Helpdesk Signature Remover',
    'summary': 'Remove Signatures of Tickets emails',
    'version': '10.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'https://odoo-community.org/',
    'author': '<Jarsa Sistemas S.A. de C.V.>',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'helpdesk',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/signature_remover_view.xml',
        'views/helpdesk_ticket_view.xml',
    ]
}
