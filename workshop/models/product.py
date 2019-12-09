# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp



class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_repair_services = fields.Boolean('Is Repair Services', default=False)

    work_center = fields.Many2one('workshop.work.centers', string='Work Center')

    service_duration = fields.Float(string='Service Duration')

    is_spare_part = fields.Boolean('Is Spare Part', default=False)
    is_workshop_consumable = fields.Boolean('Is Workshop Consumable', default=False)


    original_part_number = fields.Char(string='Original Part Number')
