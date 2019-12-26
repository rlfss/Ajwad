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
    margin = fields.Float('Margin', digits=0, store=True, compute='_compute_margin')
    margin_percent = fields.Float('Margin Percent', digits=0, store=True, compute='_compute_margin')



    @api.onchange('sale_price')
    def _compute_margin(self):
        for line in self:
            if line.sale_price > line.final_cost :
                line.margin = line.sale_price - line.final_cost
                line.margin_percent = ((line.sale_price - line.final_cost) / line.sale_price) * 100


# class StockLandedCost(models.Model):
#     _inherit = "stock.landed.cost"

#     landed_cost_pricing = fields.One2many('landed.cost.pricing', 'cost_id', 'Landed Cost Pricing')


#     @api.multi
#     def compute_landed_pricing_cost(self):
#         PricLines = self.env['landed.cost.pricing']
#         PricLines.search([('cost_id', 'in', self.ids)]).unlink()
#         for move in self.mapped('picking_ids').mapped('move_lines'):
#             AdjustementLines = self.env['stock.valuation.adjustment.lines'].search([('cost_id', 'in', self.ids)])
#             digits = dp.get_precision('Product Price')(self._cr)
#             additionalcost = 0.0
#             quantity = 0.0
#             sale_price = 0.0
#             for adj in AdjustementLines:
#                 product = move.product_id.id
#                 sale_price = move.product_id.list_price 
#                 quantity = move.product_qty
#                 former_cost = move.value
#                 if adj.product_id.id == product:
#                     addcost = adj.additional_landed_cost
#                     additionalcost += tools.float_round(addcost, precision_digits=digits[1]) if digits else addcost
#                     newadditi = additionalcost / quantity
#                     final_cost = newadditi + former_cost
#             vals = {'cost_id': self.id, 'product_id': product, 'former_cost': former_cost,'additional_landed_cost': newadditi,'final_cost': final_cost,'sale_price': sale_price}
#             return_obj = self.env['landed.cost.pricing'].create(vals)
#             print(return_obj)



