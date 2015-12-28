# -*- coding: utf-8 -*-
from openerp import models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    def action_base_config_settings(self, cr, uid, context=None):
        res = self.create(cr, uid, {'auth_signup_uninvited': True},
                          context=context)
        self.execute(cr, uid, [res], context=context)
        return True
