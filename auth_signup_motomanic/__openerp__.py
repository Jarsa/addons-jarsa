# -*- coding: utf-8 -*-
{
    "name": "Auth Signup Motomanic",
    "version": "8.0.1.0.0",
    "category": "base",
    "author": "Jarsa Sistemas, S.A. de C.V.,Odoo Community Association (OCA)",
    "website": "www.jarsa.com.mx",
    "license": "AGPL-3",
    "depends": [
        'auth_signup',
        'fleet',
        'website',
    ],
    "summary": "",
    "data": [
        'data/fleet_vehicle_year_data.xml',
        'views/auth_signup_login.xml',
        'views/base_config_settings.xml',
        'views/fleet_vehicle_model_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    "application": True,
    "installable": True,
}
