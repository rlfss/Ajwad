# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp



class WorkShopRepair(models.Model):
    _name = 'workshop.repair'
    _description = 'WorkShop Repair Orders'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopWorkOrders(models.Model):
    _name = 'workshop.work.orders'
    _description = 'Work Orders'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))





class WorkShopTechnicians(models.Model):
    _name = 'workshop.technicians'
    _description = 'Technicians'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))




class WorkShopRepairServices(models.Model):
    _name = 'workshop.repair.services'
    _description = 'Repair Services'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))





class WorkShopWorkCenters(models.Model):
    _name = 'workshop.work.centers'
    _description = 'Work Centers'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))


