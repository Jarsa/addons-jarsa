from openerp import models, fields
import urllib
from lxml import etree


class product_product(models.Model):
	_name = 'product_product'
	_inherit = 'product.product'

	brand_id = fields.Many2one('product.brand', string='Brand')
	manufacturer_code = fields.Char()
	supplier_local_avialable = fields.Iteger()
	supplier_distribution_center = fields.Iteger()

	

url = 'http://www.grupocva.com/catalogo_clientes_xml/lista_precios.xml?cliente=40762&marca=%25&grupo=%25&clave=%25&codigo=%25'
file = urllib.urlopen(url)
data = file.read()
file.close()
root = etree.XML(data)
count = 1
for item in root:
    print count, item.findtext('clave')
    count += 1