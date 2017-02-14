# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'HelpDesk Task Creation',
    'version': '10.0.0.1.0',
    'category': 'Project',
    'author': 'Jarsa Sistemas',
    'website': 'https://www.jarsa.com.mx',
    'depends': ['helpdesk', 'project'],
    'summary': (
        'Create / Assign Task from Helpdesk tickets.'),
    'description': (
        'Create / Assign Task from Helpdesk tickets.'),
    'license': 'AGPL-3',
    'data': [
        'wizards/ticket_assignation_wizard_view.xml',
        'views/project_task_view.xml',
        'views/helpdesk_ticket_view.xml',
    ],
    'application': True,
    'installable': True,
}
