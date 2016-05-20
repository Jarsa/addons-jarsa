# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestCvaConfigSettings(TransactionCase):
    """
    This will test model product product
    """
    def setUp(self):
        """
        Define global variables
        """
        super(TestCvaConfigSettings, self).setUp()
        self.group = self.env['cva.group']
        self.cva = self.env['cva.config.settings']

    def test_10_cva_config_settings_set_allowed_groups(self):
