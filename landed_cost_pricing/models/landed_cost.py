# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError


class LandedCost(models.Model):
    _inherit = "stock.landed.cost"

    landed_cost_pricing = fields.One2many('landed.cost.pricing', 'cost_id', 'Landed Cost Pricing')


    @api.multi
    def compute_landed_pricing_cost(self):
        PricLines = self.env['landed.cost.pricing']
        PricLines.search([('cost_id', 'in', self.ids)]).unlink()
        for move in self.mapped('picking_ids').mapped('move_lines'):
            AdjustementLines = self.env['stock.valuation.adjustment.lines'].search([('cost_id', 'in', self.ids)])
            digits = dp.get_precision('Product Price')(self._cr)
            additionalcost = 0.0
            quantity = 0.0
            sale_price = 0.0
            for adj in AdjustementLines:
                product = move.product_id.id
                sale_price = move.product_id.list_price 
                quantity = move.product_qty
                former_cost = move.value
                if adj.product_id.id == product:
                    addcost = adj.additional_landed_cost
                    additionalcost += tools.float_round(addcost, precision_digits=digits[1]) if digits else addcost
                    newadditi = additionalcost / quantity
                    newformer_cost = former_cost / quantity
                    final_cost = newadditi + newformer_cost
            vals = {'cost_id': self.id, 'product_id': product, 'former_cost': newformer_cost,'additional_landed_cost': newadditi,'final_cost': final_cost,'sale_price': sale_price}
            return_obj = self.env['landed.cost.pricing'].create(vals)
            print(return_obj)
