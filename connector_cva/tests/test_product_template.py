# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from mock import MagicMock
from lxml import etree
import requests


class TestProductTemplate(TransactionCase):
    """
    This will test model product.template
    """
    def setUp(self):
        """
        Define global variables
        """
        super(TestProductTemplate, self).setUp()
        self.cva = self.env['cva.config.settings']
        self.xml = requests.get('http://localhost:8069/connector_cva/static/'
                                'src/xml/test.xml').content

    def test_10_update_price_multi(self):
        """
            test for methos update_price_multi
        """
        product_tem = self.cva.create_product(etree.XML(self.xml)[1])
        product = product_tem.with_context(
            {'active_ids': product_tem.ids})
        product.update_price_multi()

        product_template = self.cva.create_product(etree.XML(self.xml)[0])
        cva = self.cva.create({
            'name': '40762',
            'main_location': self.env.ref('connector_cva.loc_torreon').id})
        cva.execute()
        cva.connect_cva = MagicMock()
        cva.connect_cva.return_value = etree.XML(self.xml)
        product = product_template.with_context(
            {'active_ids': product_template.ids})
        product.write({
            'standard_price': 0.00,
        })
        product.update_price_multi()
        self.assertEqual(product.standard_price, 114.94,
                         'Product is not Update')
