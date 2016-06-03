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
        """
            test for methods get_products, update_product_qty
            and connect_cva.
        """
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id,
            'allowed_groups': [(0, 0, {'name': 'AIRE ACONDICIONADO'})],
        })
        cva.execute()
        cva.get_products()
        product = self.obj_product.search([('default_code', '=', 'AA-63')])
        self.assertEqual(
            product.name,
            'AIRE ACONDICIONADO TRIPPLITE SRCOOL7KRM, '
            'PARA INSTALAR EN RACK SMARTRACK 7,000 BTU 120V',
            'Product is not create'
        )

    def test_20_cva_config_settings_get_groups(self):
        """
            test for method get_groups
        """
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id})
        cva.execute()
        cva.connect_cva = MagicMock()
        cva.connect_cva.return_value = etree.XML(self.xml)
        cva.get_groups()
        group = self.env['cva.group']
        group_list = [x.name for x in group.search([])]
        self.assertEqual(group_list, ['BACK PACK (MOCHILA)'],
                         'Group is not create')
        cva.get_products()

    def test_30_cva_config_settings_update_product_cron(self):
        """
            test for method update_product_cron
        """
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id,
            'allowed_groups': [(0, 0, {'name': 'BACK PACK (MOCHILA)'})],
        })
        cva.execute()
        cva.connect_cva = MagicMock()
        cva.connect_cva.return_value = etree.XML(self.xml)
        cva.get_products()
        product = self.obj_product.search([('default_code', '=', 'AC-3589')])
        product.write({'standard_price': 0.00})
        cva.update_product_cron()
        self.assertEqual(product.standard_price, 114.94,
                         'Product is not Update')
        cva.connect_cva.return_value = ''
        cva.update_product_cron()

    def test_40_cva_config_settings_create_products(self):
        """
            test for method create_product. create product - image
            and create product - not image
        """
        product_image = self.cva.create_product(etree.XML(self.xml)[0])
        if product_image.image_medium is not False:
            image = True
            self.assertEqual(image, True, 'Product not with image')
        product_not_image = self.cva.create_product(etree.XML(self.xml)[1])
        self.assertEqual(product_not_image.image_medium, False,
                         'Product with image')
