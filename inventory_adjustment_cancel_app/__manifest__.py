# -*- coding: utf-8 -*-
{
    'name': 'Inventory Adjustment Cancel',
    "author": "Edge Technologies",
    'version': '12.0.1.0',
    'live_test_url': "https://youtu.be/PGArGYyjM90",
    "images":['static/description/main_screenshot.png'],
    'summary': "This app helps user to cancel inventory adjustment even if in validated state. Stock journal entry and product quantity will also cancceled while inventory adjustment cancelled.",
    'description': """This app helps user to cancel inventory adjustment even if in validated state. Stock journal entry will cancelled and product quantity will also update while cancel inventory adjustment. 
Cancel inventory adjustment apps allow to cancel opening stock and other inventory adjustment quickly even if in validated state. If you are using real time inventory valudation then its also cancelled Stock journal entry and product quantity will also update while cancel inventory adjustment.This apps can be use when use can make mistake while adjust product stock or while importing/adding stock of product and user validated inventory adjustment after that on Odoo there is ractify option. Our apps helps to ractify opening stock as well as inventory adjustment on Odoo ERP at any stage and user can set it draft and have chance to correct it. Don't worry all the stock balance/quant and accounting entries will be effected properly.stock inventory cancel stock adjustment reverse stock adjustment reverse cancel adjustment of inventory reset to draft reverse inventory adjustment cancel inventory adjustment reverse cancel inventory stock adjustment reverse inventory stock adjustment cancel stock inventory adjustment reverse stock inventory adjustment reset stock inventory adjustment reset inventory adjustment on warehouse reset inventory stock adjustment Odoo. odoo cancel stock adjustment Odoo cancel inventory adjustment cancel 

""",
    "license" : "OPL-1",
    'depends': ['base','sale_management','stock','account','purchase','stock_account','account_cancel'],
    'data': [
            'views/inventory_views.xml',
            ],
    'installable': True,
    'auto_install': False,
    'price': 14,
    'currency': "EUR",
    'category': 'Warehouse',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
