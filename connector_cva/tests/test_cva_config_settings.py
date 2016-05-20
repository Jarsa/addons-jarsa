# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from mock import MagicMock
from lxml import etree


class TestCvaConfigSettings(TransactionCase):
    """
    This will test model cva config settings
    """
    def setUp(self):
        """
        Define global variables
        """
        super(TestCvaConfigSettings, self).setUp()
        self.cva = self.env['cva.config.settings']

    def test_10_cva_config_settings_get_products(self):
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id,
            'allowed_groups': [(0, 0, {'name': 'AIRE ACONDICIONADO'})],
        })
        cva.execute()
        cva.get_products()

    def test_20_cva_config_settings_get_groups(self):
        xml = ('<articulos><item><grupo>BACK PACK (MOCHILA)</grupo></item>'
               '</articulos>')
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id})
        cva.execute()
        cva.connect_cva = MagicMock()
        cva.connect_cva.return_value = etree.XML(xml)
        cva.get_groups()
