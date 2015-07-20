# -*- encoding: utf-8 -*-
from openerp import fields, models, api, _
import requests
from lxml import etree
import base64
import ipdb


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
        """
            Connect to CVA web-services
            @param params: dict with parameters to generate xml file
            @return: returns a xml object
        """   
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
                
    @api.multi
    def create_product(self, item):
        product_obj = self.env['product.template']
        category_obj = self.env['product.public.category']
        category = category_obj.search(['|', ('name', '=', item.findtext('grupo')), ('name', '=', item.findtext('subgrupo'))])
        if not item.findtext('imagen'):
            image = False
        else:
            image = base64.encodestring(requests.get(item.findtext('imagen')).content)
        if item.findtext('moneda') == 'Dolares':
            price = float(item.findtext('precio')) * float(item.findtext('tipocambio'))
        else:
            price = float(item.findtext('precio'))
        product_obj.create({'name': item.findtext('descripcion'),
                            'default_code': item.findtext('clave'), # + '/' + item.findtext('codigo_fabricante'),
                            'standard_price': price,
                            'public_categ_ids': [(6, 0, [x.id for x in category])],
                            'description': _('Ficha comercial\n') + 
                                           item.findtext('ficha_comercial') + '\n\n' +
                                           _('Ficha tecnica\n') + item.findtext('ficha_tecnica'),
                            'image_medium': image,
                            })

    @api.multi
    def update_product(self, item):
        product_obj = self.env('product.template')
        if item.findtext('moneda') == 'Dolares':
            price = float(item.findtext('precio')) * float(item.findtext('tipocambio'))
        else:
            price = float(item.findtext('precio'))
        product_obj.write({
                           'standard_price': price
                          })
    
    @api.one
    def get_products(self):
        ipdb.set_trace()
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
                      'dc': '1',
                      'tc': '1',
                      'subgpo': '1',}
            root = self.connect_cva(params)
            for item in root:
                if item.findtext('clave') not in product_list:
                    if int(item.findtext('disponible')) > 0 and self.avialable == True:
                        self.create_product(item)
                    elif int(item.findtext('disponibleCD')) > 0 and self.avialable_dc == True:
                        self.create_product(item)
                    elif self.all_products == True:
                        self.create_product(item)

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
