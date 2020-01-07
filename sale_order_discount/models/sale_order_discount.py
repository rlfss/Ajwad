# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class PurchaseCustomOrderLine(models.Model):
    _inherit = 'sale.order'

    global_discount = fields.Float(string='Global Discount', digits=dp.get_precision('Discount'), default=0.0)
    global_discount_type = fields.Selection([('fixed', 'Fixed'),('percent ', 'Percent ')], string="Discount Type")
    total_global_discount  = fields.Float(string='Global Discount Total', digits=dp.get_precision('Discount'), default=0.0)
    total_undiscount = fields.Float(string='UnDiscounted Total', digits=dp.get_precision('Discount'), default=0.0, compute='_total_undiscount')

    def _total_undiscount(self):
        for order in self:
            for line in order.order_line:
                order.total_undiscount += line.price_unit
            

    @api.onchange('global_discount_type')
    def _discount_type(self):
        for order in self:
            order.global_discount = 0
            

    @api.onchange('global_discount')
    def _discount_amount_total(self):
        for order in self:
            total_undiscount = 0.0
            for line in order.order_line:
                total_undiscount += line.price_unit
            discount_limit = order.team_id.discount_limit
            discount_limit_total = total_undiscount  * discount_limit / 100
            
            if order.global_discount_type == 'fixed':
                if total_undiscount - order.amount_total < order.global_discount:
                    order.total_global_discount = order.global_discount
                else:
                    raise ValidationError('Discount Value Greater Than Discount Limit' + ' ' + str(discount_limit_total))                
            if order.global_discount_type == 'percent':
                discount = sum(order.order_line.mapped('price_subtotal')) * order.global_discount / 100
                if total_undiscount - order.amount_total < discount:
                    order.total_global_discount = discount
                else:
                    raise ValidationError('Discount Value Greater Than Discount Limit' + ' ' + str(discount_limit_total))                
