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

    name = fields.Char('Name')
    street = fields.Char('Street')
    mobile = fields.Char('Mobile')

    related_partner = fields.Many2one('res.partner', string='Related Partner', required=True)
    related_employee = fields.Many2one('hr.employee', string='Related Employee', required=True)


class WorkShopWorkCenters(models.Model):
    _name = 'workshop.work.centers'
    _inherit = ['mail.thread']
    _description = 'Work Centers'

    name = fields.Char('Name')
    code = fields.Char('Code')

    technicians = fields.Many2many('workshop.technicians', string='Technicians List', required=True)
    partner_id = fields.Many2one('res.partner', related='technicians.related_partner', string='Related Partner')
    
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    operations_type = fields.Many2one('stock.picking.type', string='Operations Type')




class WorkShopCarCheckOut(models.Model):
    _name = 'workshop.car.checkout'
    _description = 'Car Check Out'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))

