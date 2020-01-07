# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp


class PurchaseCustomOrderLine(models.Model):
    _inherit = 'sale.order'

    global_discount = fields.Float(string='Global Discount', digits=dp.get_precision('Discount'), default=0.0)
    global_discount_type = fields.Selection([('fixed', 'Fixed'),('percent ', 'Percent ')], string="Discount Type")

    