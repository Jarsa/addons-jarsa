# -*- encoding: utf-8 -*-
from openerp import fields, models, api


class ZkWizard(models.TransientModel):
    _name = 'zk.wizard'

    @api.multi
    def get_attendance_log(self):
        self.env['zk.device'].get_attendace_log()
