# -*- coding: utf-8 -*-
from openerp import models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    @api.multi
    def action_stock_config_settings(self):
        res = self.create(
            {'group_stock_multiple_locations': 1}
            )

        self.execute([res])
        return 1