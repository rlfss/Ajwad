from odoo import models, fields


class StockLandedCostInherit(models.Model):
    _inherit = 'stock.landed.cost'

    shipment_reference = fields.Char('Shipment Reference', help="Shipment Reference")





