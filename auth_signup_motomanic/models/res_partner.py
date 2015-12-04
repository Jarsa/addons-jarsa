# -*- coding: utf-8 -*-
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_ids = fields.One2many(
        'fleet.vehicle', 'driver_id', string='Vehicles')
