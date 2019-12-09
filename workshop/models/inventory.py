# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp




class WorkShopSparePartsRequests(models.Model):
    _name = 'workshop.spare.parts.requests'
    _description = 'Spare Parts Requests'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopProcurementRequests(models.Model):
    _name = 'workshop.procurement.requests'
    _description = 'Procurement Requests'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))


class WorkShopConsumableDeliveries(models.Model):
    _name = 'workshop.consumable.deliveries'
    _description = 'Consumable Deliveries'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



