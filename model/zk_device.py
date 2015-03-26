# -*- encoding: utf-8 -*-
from openerp import fields, models
import zkemapi


class zk_device(models.Model):
    _name = 'zk.device'
    _description = 'ZKTeco Device'
    name = fields.Char(string='Device Name', size=64, required=True)
    host = fields.Char(string='Host/IP Address', required=True, default='192.168.1.201')
    number = fields.Integer('Device Number', required=True)
    port = fields.Integer('Port', required=True, default=4370)
    timezone = fields.Integer('Time Zone', required=True, default=-6)

# device = zkemapi.zkem()
# host = '192.168.0.50'
# connect = device.connect(host)