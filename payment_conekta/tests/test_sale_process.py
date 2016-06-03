# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestUi(openerp.tests.HttpCase):
    def test_10_admin_checkout(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour'].run('shop_buy_prod_conekta',"
            " 'test')",
            "odoo.__DEBUG__.services['web.Tour'].tours.shop_buy_prod_conekta",
            login="admin")

    def test_20_demo_checkout(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour'].run('shop_buy_prod_conekta'"
            ", 'test')",
            "odoo.__DEBUG__.services['web.Tour'].tours.shop_buy_prod_conekta",
            login="demo")

    def test_30_public_checkout(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web.Tour'].run('shop_buy_prod_conekta'"
            ", 'test')",
            "odoo.__DEBUG__.services['web.Tour'].tours.shop_buy_prod_conekta"
        )
