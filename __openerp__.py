# -*- encoding: utf-8 -*-
{
    "name": "Connector ZK Biometric Devices",
    "version": "1.0",
    "category": "Connector",
    "author": "Jarsa Sistemas, S.A. de C.V.",
    "website": "www.jarsa.com.mx",
    "depends": ['hr_attendance'],
    "summary": "Integation with ZKTeco devices",
    "description": """
                    This module adds functionality to:
                    * Import data from users

                    Depends on module zkemapi downloaded from:

                    https://bitbucket.org/johnmc/zkemapi/overview

                    """,
    "data": ['views/zk_device_view.xml',
             'views/hr_employee_view.xml',
             'data/ir_cron.xml',],
    "application": True,
    "installable": True,
}
