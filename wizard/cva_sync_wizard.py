# -*- encoding: utf-8 -*-
from openerp import fields, models, _, api
import urllib
from lxml import etree


class cva_sync(models.TransientModel):
	_name = 'cva.sync'
	_description = _('CVA Sincronization')

	name = fields.Char()

	@api.one
	def get_all_products(self):
		product = self.env['product.product']
		category = self.env['product.public.category']
		product_list = [x.default_code for x in product.search([])]
		url = 'http://www.grupocva.com/catalogo_clientes_xml/lista_precios.xml?cliente=40762&marca=%&grupo=%&clave=%&codigo=%&tc=1'
		file = urllib.urlopen(url)
		data = file.read()
		file.close()
		root = etree.XML(data)
		count = 1
		for item in root:
			print count
			count += 1
			if item.findtext('disponible') != 0:
				category_list = [x.name for x in category.search([])]
				if item.findtext('grupo') not in category_list:
					category.create({'name': item.findtext('grupo')})
				categ_id = category.search([('name', '=', item.findtext('grupo'))]).id
				if item.findtext('clave') in product_list:
					product_id = product.search([('default_code', '=', item.findtext('clave'))])
					if item.findtext('moneda') == 'Dolares':
						product_id.write({'standard_price': float(item.findtext('precio')) * float(item.findtext('tipocambio')),
									 	  'public_categ_ids': [4, categ_id, 0],
									 	  })
					else:
						product_id.write({'standard_price': item.findtext('precio'),
									 	  'public_categ_ids': [4, categ_id, 0],
									 	  })
				elif item.findtext('moneda') == 'Dolares':
					product.create({'name': item.findtext('descripcion'),
				 					'default_code': item.findtext('clave'),
				 					'standard_price': float(item.findtext('precio')) * float(item.findtext('tipocambio')),
				 					'public_categ_ids': [4, categ_id, 0],
				 					})
				else:
				 	product.create({'name': item.findtext('descripcion'),
				 					'default_code': item.findtext('clave'),
				 					'standard_price': item.findtext('precio'),
				 					'public_categ_ids': [4, categ_id, 0],
				 					})
