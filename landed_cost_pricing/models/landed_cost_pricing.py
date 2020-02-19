# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError

class LandedCostPricing(models.Model):
    _name = 'landed.cost.pricing'
    _description = 'Landed Cost Pricing'

    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost',ondelete='cascade', required=False)
    product_id = fields.Many2one('product.product', 'Product', required=False)
    former_cost = fields.Float('Former Cost(Per Unit)', digits=dp.get_precision('Product Price'))
    additional_landed_cost = fields.Float('Additional Landed Cost',digits=dp.get_precision('Product Price'))
    final_cost = fields.Float('New Cost', digits=0, store=True)
    sale_price = fields.Float('Sale Price', digits=0, store=True)
    margin = fields.Float('Margin')
    margin_percent = fields.Float('Margin Percent')

    product_qty = fields.Float('product qty', digits=0, store=True)

    @api.onchange('sale_price')
    def _compute_margin(self):
        for line in self:
            if line.sale_price > line.final_cost :
                line.margin = line.sale_price - line.final_cost
                line.margin_percent = ((line.sale_price - line.final_cost) / line.sale_price) * 100

    @api.onchange('margin')
    def _compute_sale_price(self):
        for line in self:
            if line.margin > 0 :
                line.sale_price = line.final_cost + line.margin
                line.margin_percent = (line.margin / (line.final_cost + line.margin)) * 100

    @api.onchange('margin_percent')
    def _compute_margin_percent(self):
        for line in self:
            if line.margin_percent > 0 :
                line.margin = (line.final_cost * line.margin_percent ) / ( 100 - line.margin_percent)
                line.sale_price = line.final_cost + ((line.final_cost * line.margin_percent ) / ( 100 - line.margin_percent))



class PricesEvaluation(models.Model):
    _name = 'landed.cost.pricing.evaluation'
    _description = 'Landed Cost Pricing Evaluation'

    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost',ondelete='cascade', required=False)
    product_id = fields.Many2one('product.product', 'Product', required=False)
    new_cost = fields.Float('New Cost', digits=dp.get_precision('Product Price'))
    old_cost = fields.Float('Old Cost', digits=dp.get_precision('Product Price'))
    new_qty = fields.Float('New Qty ', digits=0, store=True)
    old_qty = fields.Float('Old Qty ', digits=0, store=True)
    onh_qty = fields.Float('Qty on Hand ', digits=0, store=True)
    avg_cost = fields.Float('Average Cost', digits=dp.get_precision('Product Price'))
    new_sale_price = fields.Float('New Sale Price', digits=0, store=True)
    old_sale_price = fields.Float('Old Sale Price', digits=0, store=True)
    new_margin = fields.Float('New Margin Amount')
    old_margin = fields.Float('Old Margin Amount')
    new_margin_percent = fields.Float('New Margin Percent')
    old_margin_percent = fields.Float('Old Margin Percent')



    @api.onchange('new_sale_price')
    def _compute_margin(self):
        for line in self:
            if line.new_sale_price > line.new_cost :
                line.new_margin = line.new_sale_price - line.new_cost
                line.new_margin_percent = ((line.new_sale_price - line.new_cost) / line.new_sale_price) * 100

    @api.onchange('new_margin')
    def _compute_sale_price(self):
        for line in self:
            if line.new_margin > 0 :
                line.new_sale_price = line.new_cost + line.new_margin
                line.new_margin_percent = (line.new_margin / (line.new_cost + line.new_margin)) * 100

    @api.onchange('new_margin_percent')
    def _compute_margin_percent(self):
        for line in self:
            if line.new_margin_percent > 0 :
                line.new_margin = (line.new_cost * line.new_margin_percent ) / ( 100 - line.new_margin_percent)
                line.new_sale_price = line.new_cost + ((line.new_cost * line.new_margin_percent ) / ( 100 - line.new_margin_percent))
