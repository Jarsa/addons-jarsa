# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from mock import MagicMock
from lxml import etree
import requests


class TestCvaConfigSettings(TransactionCase):
    """
    This will test model cva config settings
    """
    def setUp(self):
        """
        Define global variables.
        """
        super(TestCvaConfigSettings, self).setUp()
        self.cva = self.env['cva.config.settings']
        self.xml = requests.get('http://localhost:8069/connector_cva/static/'
                                'src/xml/test.xml').content
        self.obj_product = self.env['product.template']

    def test_10_cva_config_settings_get_products(self):
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id,
            'allowed_groups': [(0, 0, {'name': 'AIRE ACONDICIONADO'})],
        })
        cva.execute()
        cva.get_products()
        product = self.obj_product.search([('default_code', '=', 'AA-63')])
        product.write({
            'standard_price': 0.00,
            })
        cva.update_product_cron()
        self.assertEqual(product.standard_price, 16571.5,
                         'Product is not Update')

    def test_20_cva_config_settings_get_groups(self):
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id})
        cva.execute()
        cva.connect_cva = MagicMock()
        cva.connect_cva.return_value = etree.XML(self.xml)
        cva.get_groups()
        group = self.env['cva.group']
        group_list = [x.name for x in group.search([])]
        self.assertEqual(
            group_list,
            ['BACK PACK (MOCHILA)'],
            'Group is not create'
        )
        cva.get_products()

    def test_30_cva_config_settings_update(self):
        self.cva.update_product_cron()
        product_template = self.cva.create_product(etree.XML(self.xml)[0])
        product = product_template.with_context(
            {'active_ids': product_template.ids})
        product.update_price_multi()
