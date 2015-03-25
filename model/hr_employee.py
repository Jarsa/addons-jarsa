# -*- encoding: utf-8 -*-
from openerp import fields, models


class hr_employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
    zk_id = fields.integer(string='ID')
