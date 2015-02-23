# -*- encoding: utf-8 -*-
from openerp import fields, models, api


class cva_config(models.Model):
	_name = 'cva.config.settings'
	name = fields.char(string='Client number')

	@api.multi
	def get_url(self, brand_name='%', ):
		url = 'http://www.grupocva.com/catalogo_clientes_xml/lista_precios.xml?cliente=%s&marca=%&grupo=%&clave=%&codigo=PT-90' % (self.name, )
		return url
