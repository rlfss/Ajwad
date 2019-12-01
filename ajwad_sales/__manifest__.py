# -*- coding: utf-8 -*-
{
        'name': 'Sales Customization Ajwad',
        'version': '12.0.1.0.0',
        'category': 'Sale',
        'author': '',
        'depends': ['base', 'sale', 'sale_order_type','sales_team'],
        'data': [
                'security/sale_groups.xml',
                'views/sale_order.xml'
        ],
        'installable': True,
        'application': False,
        'auto_install': False,
}
