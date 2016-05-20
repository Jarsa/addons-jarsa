# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestCvaConfigSettings(TransactionCase):
    """
    This will test model cva config settings
    """
    def setUp(self):
        """
        Define global variables
        """
        super(TestCvaConfigSettings, self).setUp()

    def test_10_cva_config_settings_get_products(self):
        cva_obj = self.env['cva.config.settings']
        cva = cva_obj.create({
            'name': '40762',
            'allowed_groups': [(0, 0, {'name': 'AIRE ACONDICIONADO'})],
        })
        cva.execute()
        cva.get_products()
