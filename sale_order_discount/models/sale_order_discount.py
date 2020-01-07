# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

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
        self.global_discount = 0
        self.total_global_discount = 0
            

    @api.onchange('global_discount')
    def _discount_amount_total(self):
        total_undiscount = 0.0
        amount_total = 0.0
        
        for line in self.order_line:
            total_undiscount += line.price_unit
            
        for line in self.order_line:
            amount_total += line.price_subtotal


        discount_limit = self.team_id.discount_limit
        discount_limit_total = total_undiscount  * discount_limit / 100
        
        
        if self.global_discount_type == 'fixed':
            discount = total_undiscount - amount_total
            alldiscount = discount + self.global_discount
            if  alldiscount <= discount_limit_total:
                self.total_global_discount = self.global_discount
                self.amount_total = amount_total - self.global_discount
            else:
                self.global_discount = 0
                self.total_global_discount = 0
                raise ValidationError('Discount Value Greater Than Discount Limit')    
                
                
        if self.global_discount_type == 'percent':
            discount = amount_total * self.global_discount / 100
            oldisc = total_undiscount - amount_total
            alldic = oldisc + discount
            raise ValidationError('discount ' + discount + ' oldisc '+ oldisc +  ' alldic ' + alldic )
            if alldic <= discount_limit_total:
                self.amount_total = amount_total - discount
            else:
                self.global_discount = 0
                self.total_global_discount = 0
                raise ValidationError('Discount Value Greater Than Discount Limit')
                
