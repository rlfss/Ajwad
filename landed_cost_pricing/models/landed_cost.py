# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError


class LandedCost(models.Model):
    _inherit = "stock.landed.cost"

    landed_cost_pricing = fields.One2many('landed.cost.pricing', 'cost_id', 'Landed Cost Pricing')
    evaluation_cost_pricing = fields.One2many('landed.cost.pricing.evaluation', 'cost_id', 'Prices Evaluation')


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
            vals = {'cost_id': self.id, 'product_id': product, 'former_cost': newformer_cost,'additional_landed_cost': newadditi,'final_cost': final_cost,'sale_price': sale_price,'product_qty': quantity}
            return_obj = self.env['landed.cost.pricing'].create(vals)
            print(return_obj)


    @api.multi
    def compute_landed_pricing_cost_evaluation(self):
        PricLines = self.env['landed.cost.pricing.evaluation']
        PricLines.search([('cost_id', 'in', self.ids)]).unlink()
        AdjustementLines = self.env['landed.cost.pricing'].search([('cost_id', 'in', self.ids)])
        digits = dp.get_precision('Product Price')(self._cr)
        new_cost = 0.0
        new_qty = 0.0
        old_cost = 0.0
        onh_qty = 0.0
        old_qty = 0.0
        avg_cost = 0.0
        old_sale_price = 0.0
        old_margin = 0.0
        old_margin_percent = 0.0
        for adj in AdjustementLines:
            product = adj.product_id.id
            new_cost = adj.final_cost 
            new_qty = adj.product_qty
            old_cost = adj.product_id.standard_price
            onh_qty = adj.product_id.qty_available
            old_qty = onh_qty - new_qty
            avg_cost = ((new_cost * new_qty) + (old_cost * old_qty))/(new_qty + old_qty) 
            old_sale_price = adj.product_id.list_price
            if old_sale_price > old_cost:
                old_margin = old_sale_price - old_cost
                old_margin_percent = old_margin / old_sale_price
            vals = {'cost_id': self.id, 'product_id': product, 'new_cost': new_cost,'new_qty': new_qty,'old_cost': old_cost,'onh_qty': onh_qty,'old_qty': old_qty,'avg_cost': avg_cost,'old_sale_price': old_sale_price,'old_margin': old_margin,'old_margin_percent': old_margin_percent}
            return_obj = self.env['landed.cost.pricing.evaluation'].create(vals)
            print(return_obj)
