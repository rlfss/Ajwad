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
    currency_id = fields.Many2one( store=True, string='Currency', readonly=True)

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

    repair_services = fields.One2many('workshop.repair.line','repair_line_id', string='Repair Services')
    spare_parts = fields.One2many('workshop.spare.parts.line', 'spare_parts_line_id', string='Spare Parts')

    amount_untaxed = fields.Float(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange', track_sequence=5)
    amount_tax = fields.Float(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total_spare = fields.Float(string='Total Spare Parts', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    amount_total_repair = fields.Float(string='Total Services', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    amount_total_order = fields.Float(string='Total Order', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)

    @api.depends('spare_parts.price_subtotal','repair_services.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed_spare = amount_tax = 0.0
            amount_untaxed_repair = amount_tax = 0.0
            for line in order.spare_parts:
                amount_untaxed_spare += line.price_subtotal
            for line in order.repair_services:
                amount_untaxed_repair += line.price_subtotal

            amount_total_order = amount_untaxed_spare + amount_untaxed_repair
            order.update({
                'amount_total_spare': amount_untaxed_spare + amount_tax,
                'amount_total_repair': amount_untaxed_repair + amount_tax,
                'amount_total_order': amount_total_order,
            })

    


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('workshop') or _('New')                
            result = super(WorkShop, self).create(vals)
            return result

class WorkShopSparePartsLine(models.Model):
    _name = 'workshop.spare.parts.line'
    _description = 'Workshop Spare Parts Order Line'
    
    spare_parts_line_id = fields.Many2one('workshop', string='Spare Parts Line Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('is_spare_part','=',True)], change_default=True, ondelete='restrict')
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    qty_delivered = fields.Float('Delivered Quantity', copy=False , store=True, digits=dp.get_precision('Product Unit of Measure'), default=0.0)
    qty_invoiced = fields.Float(string='Invoiced Quantity', store=True, readonly=True, digits=dp.get_precision('Product Unit of Measure'))
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    tax_id = fields.Many2one('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(price, line.spare_parts_line_id.currency_id, line.product_uom_qty)
            line.update({
                'price_subtotal': taxes['total_excluded'],
            })

    @api.onchange('product_id')
    def _prepare_line(self):
        for line in self:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price

class WorkShopRepairLine(models.Model):
    _name = 'workshop.repair.line'
    _description = 'Workshop Repair Order Line'
    
    repair_line_id = fields.Many2one('workshop', string='Spare Parts Line Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('is_repair_services','=',True)], change_default=True, ondelete='restrict')
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    qty_delivered = fields.Float('Delivered Quantity', copy=False , store=True, digits=dp.get_precision('Product Unit of Measure'), default=0.0)
    qty_invoiced = fields.Float(string='Invoiced Quantity', store=True, readonly=True, digits=dp.get_precision('Product Unit of Measure'))
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    tax_id = fields.Many2one('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    work_center = fields.Text(string='Work Center',store=True)
    service_duration = fields.Float(string='Service Duration',store=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    technicians = fields.Many2one('workshop.technicians', string='Technicians')


    @api.onchange('product_id')
    def _prepare_line(self):

        res = {}
        selected = []
        technicians = self.env['workshop.technicians'].search([])
        for tech in technicians:
            if tech.name == self.product_id.work_center.technicians.name:
                selected.append(tech.name)
        res.update({'domain':{'technicians':[('name','=',list(set(selected)))],}})


        for line in self:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price
            self.work_center = self.product_id.work_center.name
            self.service_duration = self.product_id.service_duration

        return res
    

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(price, line.repair_line_id.currency_id, line.product_uom_qty)
            line.update({
                'price_subtotal': taxes['total_excluded'],
            })


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

    name = fields.Char('Name', readonly=True , compute='_compute_name' )

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

    def _compute_name(self):
        for name1 in self:
            name1.name = name1.make.name +" " + name1.model.name



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

    name = fields.Char('Color')


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