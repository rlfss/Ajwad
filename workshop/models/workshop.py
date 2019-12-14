# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp
from datetime import datetime, timedelta

class WorkShop(models.Model):
    _name = 'workshop'
    _description = 'WorkShop Orders'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))

    vehicle = fields.Many2one('workshop.vehicles', string='Vehicle', required=True)

    make = fields.Many2one('workshop.vehicles.make', related='vehicle.make', string='Make', readonly=True)
    model = fields.Many2one('workshop.vehicles.model', related='vehicle.model', string='Model', readonly=True)
    color = fields.Many2one('workshop.vehicles.color', related='vehicle.color',  string='Color', readonly=True)

    year = fields.Integer(string='Year', related='vehicle.year', readonly=True) 

    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('gas', 'Gas'),
        ('electric', 'Electric'),
    ], related='vehicle.fuel_type', string="Fuel Type", readonly=True)

    odometer = fields.Integer(string='Last Odometer', related='vehicle.odometer') 

    liscence_plate = fields.Char('Liscence Plate', related='vehicle.liscence_plate', readonly=True)
    last_owner = fields.Many2one('res.partner', related='vehicle.last_owner', string='Last Owner', readonly=True)
    vin = fields.Char('VIN', size=17, related='vehicle.vin', readonly=True)


    customer = fields.Many2one('res.partner', string='Customer', required=True)

    adress = fields.Char('Customer Adress', related='customer.street', readonly=True)
    phone = fields.Char('Customer Phone', related='customer.phone', readonly=True)

    customer_note = fields.Text('Customer Notes')
    tecnical_note = fields.Text('Technical Notes')

    repair_services = fields.Many2many('product.template', string='Repair Services', domain=[('is_repair_services','=',True), ('type', '=', 'service')])
    spare_parts = fields.Many2many('product.template', string='Spare Parts', domain=[('is_spare_part','=',True), ('type', '=', 'product')])


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('workshop') or _('New')                
            result = super(WorkShop, self).create(vals)
            return result

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