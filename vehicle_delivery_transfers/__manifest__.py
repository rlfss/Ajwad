
{
    'name': 'Vehicle Delivery',
    'version': '1.0',
    'summary': 'Vehicle Delivery',
    'description': "",
    'depends': ['stock_account', 'purchase_stock'],
    'category': 'Warehouse',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/stock_vehicle_delivery_views.xml',
        'data/vehicle_delivery_data.xml',
        'report/vehicle_delivery_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
