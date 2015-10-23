# -*- encoding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import except_orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)
try:
    import zkemapi
except ImportError:
    _logger.debug('Can not `import zkemapi`.')


class ZkDevice(models.Model):
    _name = 'zk.device'
    _description = 'ZKTeco Device'
    name = fields.Char(
        string='Device Name',
        size=64,
        required=True)
    host = fields.Char(
        string='Host/IP Address',
        required=True,
        default='192.168.1.201')
    number = fields.Integer(
        'Device Number',
        required=True)
    port = fields.Integer(
        'Port',
        required=True,
        default=4370)
    timezone = fields.Integer(
        'Time Zone',
        required=True,
        default=-6)

    @api.multi
    def connect_device(self):
        host = self.host
        port = self.port
        device = zkemapi.zkem()
        connect = device.connect(host=host, port=port)
        if connect:
            raise except_orm(_('Success!'),
                             _('Connection completed successfully'))
        else:
            raise except_orm(_('Connection Failed!'),
                             _('Please review parameters'))

    def get_attendace_log(self, cr, uid):
        attendance = self.pool['hr.attendance']
        employee = self.pool['hr.employee']
        devices_ids = self.search(cr, uid, [])
        for zk_device in self.browse(cr, uid, devices_ids, context=None):
            host = zk_device.host
            port = zk_device.port
            timezone = -zk_device.timezone
            device = zkemapi.zkem()
            connect = device.connect(host=host, port=port)
            get_attendace_log = device.get_attendance_log()
            attendance_log = device.unpack_attendance_log()
            for log in attendance_log:
                employee_id = employee.search(
                    cr, uid, [('zk_id', '=', log[0])])
                if not employee_id:
                    raise except_orm(_('Error!'),
                                     _('There is no employee with ID %s')
                                     % log[0])
                date = log[1] + timedelta(hours=timezone)
                attendance_ids = attendance.search(
                    cr, uid, [('employee_id', '=', employee_id[0])])
                last_id = attendance_ids and max(attendance_ids)
                attendance_obj = attendance.browse(
                    cr, uid, last_id, context=None)
                if not attendance_obj:
                    sign = 'sign_in'
                elif attendance_obj[0].action == 'sign_in':
                    sign = 'sign_out'
                else:
                    sign = 'sign_in'
                attendance.create(
                    cr, uid, {'employee_id': employee_id[0],
                              'name': datetime.strftime(date, dt),
                              'action': sign,
                              })
            device.clear_attendance_log()
