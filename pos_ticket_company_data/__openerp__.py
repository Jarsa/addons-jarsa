# -*- encoding: utf-8 -*-

{   
    "name"        : "Point of Sale Ticket Company data",
    "version"     : "8.0.0.1.0",
    "category"    : "Point of Sale",
    "author"      : "Jarsa Sistemas, S.A. de C.V.",
    "website"     : "www.jarsa.com.mx",
    "depends"     : ['point_of_sale'],
    "summary"     : "Add address and VAT fields to POS ticket",
    "data" : [
        'views/pos_ticket_company_data.xml'
    ],
    "qweb" : [
        'static/src/xml/pos.xml',
    ],
    "application": True,
    "installable": True,
}