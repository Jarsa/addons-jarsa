# -*- coding: utf-8 -*-
from openerp import models, fields


class FleetVehicleYear(models.Model):
    _name = 'fleet.vehicle.year'

    name = fields.Integer(string='Year')
    model_ids = fields.Many2many('fleet.vehicle.model')
