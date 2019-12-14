# -*- coding: utf-8 -*-
{
    'name': 'Work Shop App',
    'version': '1.0',
    'depends': ['base','sale','product','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/workshop.xml',
        'views/repairs.xml',
        'views/inventory.xml',
        'views/product.xml',
        'data/sequence.xml'
    ],
    'installable': True,
}
