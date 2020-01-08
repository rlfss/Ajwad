# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class PurchaseCustomOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    initial_price_unit = fields.Float(string='Initial Unit Price', digits=dp.get_precision('Product Price'),compute='onchange_partner_recipient')
    support = fields.Float(string='Support', digits=dp.get_precision('Product Price'))

    @api.onchange('price_unit','support')
    def onchange_partner_recipient(self):
        for line in self:
            line.initial_price_unit = line.price_unit + line.support


# class StockQuant(models.Model):
#     _inherit = 'stock.quant'

#     lot_id = fields.Many2one(
#         'stock.production.lot', 'Lot/Serial Number',
#         ondelete='set null', readonly=False)
#     quantity = fields.Float(
#         'Quantity',
#         help='Quantity of products in this quant, in the default unit of measure of the product',
#         readonly=False, required=True, oldname='qty')
#     reserved_quantity = fields.Float(
#         'Reserved Quantity',
#         default=0.0,
#         help='Quantity of reserved products in this quant, in the default unit of measure of the product',
#         readonly=False, required=True)
#     location_id = fields.Many2one(
#         'stock.location', 'Location',
#         auto_join=True, ondelete='restrict', readonly=False, required=True, index=True)

#     product_id = fields.Many2one(
#         'product.product', 'Product',
#         ondelete='restrict', readonly=False, required=True, index=True)
