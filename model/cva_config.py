# -*- encoding: utf-8 -*-
from openerp import fields, models, api
import requests
from lxml import etree


class cva_config(models.Model):
    _name = 'cva.config.settings'
    name = fields.Char(string='Client number')
    url = fields.Char(string='URL', default='http://www.grupocva.com/catalogo_clientes_xml/lista_precios.xml')
    allowed_groups = fields.Many2many('product.public.category', string='Allowed groups')
    avialable = fields.Boolean(string='Get avialable products')
    avialable_dc = fields.Boolean(string='Get avialable products in Distribution Center')
    all_products = fields.Boolean(string='Get all products')

    @api.multi
    def connect_cva(self, params):
        data = requests.get(self.url, params=params).content
        root = etree.XML(data)
        return root

    @api.multi
    def get_categories(self):
        category = self.env['product.public.category']
        category_list = [x.name for x in category.search([])]
        params = {'cliente': self.name, 
                  'subgpo': '1'}
        root = self.connect_cva(params)
        for item in root:
            if item.findtext('grupo') not in category_list:
                category.create({'name': item.findtext('grupo')})
                category_list.append(item.findtext('grupo'))
            if item.findtext('subgrupo') not in category_list:
                parent_id = category.search([('name', '=', item.findtext('grupo'))]).id
                category.create({'name': item.findtext('subgrupo'),
                                 'parent_id': parent_id})
                category_list.append(item.findtext('subgrupo'))
                

    @api.one
    def get_products(self):
        product = self.env['product.product']
        category_list = []
        for x in self.allowed_groups:
            if x.parent_id:
                category_list.append(x.parent_id.name)
            else:
                category_list.append(x.name)
        category_list = list(set(category_list))
        product_list = [x.default_code for x in product.search([])]
        for category in category_list:
            params = {'cliente': self.name,
                      'grupo': category,
                      'depto': '1',
                      'dt': '1',
                      'dc': '1'}
            root = self.connect_cva(params)
            for item in root:
                if int(item.findtext('disponible')) > 0 and self.avialable == True:
                    print 'TRC', item.findtext('disponible'), item.findtext('descripcion')
                elif int(item.findtext('disponibleCD')) > 0 and self.avialable_dc == True:
                    print 'CD', item.findtext('disponibleCD'), item.findtext('descripcion')
                elif self.all_products == True:
                    print 'SE VAN A GUARDAR TODOS LOS PRODUCTOS'
                #if item.findtext('disponible') != 0:
                #    category_list = [x.name for x in category.search([])]
                #    if item.findtext('grupo') not in category_list:
                #        category.create({'name': item.findtext('grupo')})
                #    categ_id = category.search([('name', '=', item.findtext('grupo'))]).id
                #    if item.findtext('clave') in product_list:
                #        product_id = product.search([('default_code', '=', item.findtext('clave'))])
                #        if item.findtext('moneda') == 'Dolares':
                #             product_id.write({'standard_price': float(item.findtext('precio')) * float(item.findtext('tipocambio')),
                #                               'public_categ_ids': [4, categ_id, 0],
                #                               })
                #         else:
                #             product_id.write({'standard_price': item.findtext('precio'),
                #                               'public_categ_ids': [4, categ_id, 0],
                #                               })
                #     elif item.findtext('moneda') == 'Dolares':
                #         product.create({'name': item.findtext('descripcion'),
                #                         'default_code': item.findtext('clave'),
                #                         'standard_price': float(item.findtext('precio')) * float(item.findtext('tipocambio')),
                #                         'public_categ_ids': [4, categ_id, 0],
                #                         })
                #     else:
                #         product.create({'name': item.findtext('descripcion'),
                #                         'default_code': item.findtext('clave'),
                #                         'standard_price': item.findtext('precio'),
                #                         'public_categ_ids': [4, categ_id, 0],
                #                         })
