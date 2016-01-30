# -*- coding: utf-8 -*-
from openerp import models, api, _


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        model_id = values.get('model_id', False)
        year_ids = values.get('year_ids', False)
        if 'model_id' in values:
            values.pop('model_id')
        if 'year_ids' in values:
            values.pop('year_ids')
        res = super(ResUsers, self)._signup_create_user(values)
        if isinstance(res, int):
            user = self.env['res.users'].browse(res)
            try:
                model_id = self.env['fleet.vehicle.model'].browse(
                    int(model_id))[0].id
            except:
                model_id = self.env.ref(
                    'auth_signup_motomanic.fleet_vehicle_model_not_defined').id
            try:
                year = self.env['fleet.vehicle.year'].browse(
                    int(year_ids))[0].name
            except:
                year = _('Not defined')
            self.env['fleet.vehicle'].create({
                'model_id': model_id,
                'license_plate': year,
                'odometer_unit': 'kilometers',
                'driver_id': user.partner_id.id
                })
        return res
