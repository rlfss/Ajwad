# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp

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