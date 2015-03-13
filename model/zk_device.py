# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
import zkemapi


class zk_device(osv.osv):
    _name = 'zk.device'
    _description = 'ZKTeco Device'
    _columns = {
        'name': fields.char('Device Name', size=64, required=True),
        'host': fields.char('Host/IP Address', required=True),
        'number': fields.integer('Device Number', required=True),
        'port': fields.integer('Port', required=True),
        'timezone': fields.integer('Time Zone', required=True),
    }
    _defaults = {
        'port': 4370,
        'timezone': -6,
        'host': '192.168.1.201',
    }

# device = zkemapi.zkem()
# host = '192.168.0.50'
# connect = device.connect(host)