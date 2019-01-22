# -*- coding: utf-8 -*-
from odoo import http

# class InventorySerialImport(http.Controller):
#     @http.route('/inventory_serial_import/inventory_serial_import/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_serial_import/inventory_serial_import/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_serial_import.listing', {
#             'root': '/inventory_serial_import/inventory_serial_import',
#             'objects': http.request.env['inventory_serial_import.inventory_serial_import'].search([]),
#         })

#     @http.route('/inventory_serial_import/inventory_serial_import/objects/<model("inventory_serial_import.inventory_serial_import"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_serial_import.object', {
#             'object': obj
#         })