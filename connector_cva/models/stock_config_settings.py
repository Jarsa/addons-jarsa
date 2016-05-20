# -*- coding: utf-8 -*-
from openerp import models, api


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    @api.model
    def action_stock_config_settings(self):
        res = self.create({'group_stock_multiple_locations': 1})
        res.execute()
        return True
