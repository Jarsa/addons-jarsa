# -*- coding: utf-8 -*-
from openerp import models, fields


class FleetVehicleModel(models.Model):
    _inherit = "fleet.vehicle.model"

    active = fields.Boolean(default=True)
    year_ids = fields.Many2many('fleet.vehicle.year', string='Year')
