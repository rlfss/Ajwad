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
        self.initial_price_unit = self.price_unit + self.support
