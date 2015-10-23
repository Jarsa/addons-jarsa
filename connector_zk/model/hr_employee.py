# -*- encoding: utf-8 -*-
from openerp import fields, models


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
    zk_id = fields.Char(string='ID')
