# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp
from datetime import datetime, timedelta

class WorkShop(models.Model):
    _name = 'workshop'
    _description = 'Work Shop Orders'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopBooking(models.Model):
    _name = 'workshop.booking'
    _description = 'Booking Orders'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopInspectionForms(models.Model):
    _name = 'workshop.inspection.forms'
    _description = 'Inspection Forms'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopEstimations(models.Model):
    _name = 'workshop.estimations'
    _description = 'Estimations'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))



class WorkShopVehicles(models.Model):
    _name = 'workshop.vehicles'
    _description = 'Vehicles'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))

    make = fields.Many2one('workshop.vehicles.make', string='Make')
    model = fields.Many2one('workshop.vehicles.model', string='Model')
    color = fields.Many2one('workshop.vehicles.color', string='Color')

    year = fields.Integer(string='Year') 

    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('gas', 'Gas'),
        ('electric', 'Electric'),
    ], string="Fuel Type")

    odometer = fields.Integer(string='Last Odometer') 

    liscence_plate = fields.Char('Liscence Plate')
    last_owner = fields.Many2one('res.partner', string='Last Owner')
    vin = fields.Char('VIN', size=17)

    _sql_constraints = [
        ('vin_uniq', 'unique (vin)', 'The VIN Must be unique !'),
    ]



class WorkShopVehiclesMake(models.Model):
    _name = 'workshop.vehicles.make'
    _description = 'Vehicles Make'

    name = fields.Char('Make')


class WorkShopVehiclesModel(models.Model):
    _name = 'workshop.vehicles.model'
    _description = 'Vehicles Model'

    name = fields.Char('Model')

class WorkShopVehiclesColor(models.Model):
    _name = 'workshop.vehicles.color'
    _description = 'Vehicles Color'

    color = fields.Char('Color')


class WorkShopInvoice(models.Model):
    _name = 'workshop.invoice'
    _description = 'WorkShop Invoices'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))

class WorkShopExpenses(models.Model):
    _name = 'workshop.expenses'
    _description = 'WorkShop Expenses'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))


class WorkShopCustomerPayments(models.Model):
    _name = 'workshop.customer.payments'
    _description = 'Customer Payments'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))




class WorkShopDailyClosingReports(models.Model):
    _name = 'workshop.daily.reports'
    _description = 'Daily Closing Reports'

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))