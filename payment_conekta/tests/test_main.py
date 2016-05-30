# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestMain(TransactionCase):
    """
    This will test controllers main
    """
    def setUp(self):
        """
        Define global variables.
        """
        super(TestMain, self).setUp()
