# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons import decimal_precision as dp



class WorkShopRepair(models.Model):
    _name = 'workshop.repair'
    _description = 'WorkShop Repair Orders'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True , default=lambda x: str('New'))
    vehicle = fields.Many2one('workshop.vehicles', string='Vehicle', required=True, ondelete='cascade')
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

    repair_order_services = fields.One2many('repair.order.repair.line','repair_line_id', string='Repair Services')
    repair_spare_parts = fields.One2many('repair.order.spare.parts.line', 'spare_parts_line_id', string='Spare Parts')

    # amount_untaxed = fields.Float(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='onchange', track_sequence=5)
    # amount_tax = fields.Float(string='Taxes', store=True, readonly=True, compute='_amount_all')
    # amount_total_spare = fields.Float(string='Total Spare Parts', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    # amount_total_repair = fields.Float(string='Total Services', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)
    # amount_total_order = fields.Float(string='Total Order', store=True, readonly=True, compute='_amount_all', track_visibility='always', track_sequence=6)

    # @api.depends('spare_parts.price_subtotal','repair_services.price_subtotal')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for order in self:
    #         amount_untaxed_spare = amount_tax = 0.0
    #         amount_untaxed_repair = amount_tax = 0.0
    #         for line in order.spare_parts:
    #             amount_untaxed_spare += line.price_subtotal
    #         for line in order.repair_services:
    #             amount_untaxed_repair += line.price_subtotal

    #         amount_total_order = amount_untaxed_spare + amount_untaxed_repair
    #         order.update({
    #             'amount_total_spare': amount_untaxed_spare + amount_tax,
    #             'amount_total_repair': amount_untaxed_repair + amount_tax,
    #             'amount_total_order': amount_total_order,
    #         })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('repair') or _('New')                
            result = super(WorkShopRepair, self).create(vals)
            return result




class RepairOrderSparePartsLine(models.Model):
    _name = 'repair.order.spare.parts.line'
    _description = 'Repair Spare Parts Order Line'
    
    spare_parts_line_id = fields.Many2one('workshop.repair', string='Spare Parts Line Reference')
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('is_spare_part','=',True)])
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    qty_delivered = fields.Float('Delivered Quantity', copy=False , store=True, digits=dp.get_precision('Product Unit of Measure'), default=0.0)
    qty_invoiced = fields.Float(string='Invoiced Quantity', store=True, readonly=True, digits=dp.get_precision('Product Unit of Measure'))
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    

    # @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.price_unit
    #         taxes = line.tax_id.compute_all(price, line.spare_parts_line_id.currency_id, line.product_uom_qty)
    #         line.update({
    #             'price_subtotal': taxes['total_excluded'],
    #         })

    @api.onchange('product_id')
    def _prepare_line(self):
        for line in self:
            self.name = self.product_id.name




class RepairOrderLine(models.Model):
    _name = 'repair.order.repair.line'
    _description = 'Repair Order Line'
    
    repair_line_id = fields.Many2one('workshop.repair', string='Spare Parts Line Reference')
    product_id = fields.Many2one('product.product', string='Product', required=True, domain=[('is_repair_services','=',True)], change_default=True, ondelete='restrict')
    name = fields.Text(string='Description')
    work_center = fields.Text(string='Work Center',store=True)
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    qty_delivered = fields.Float('Delivered Quantity', copy=False , store=True, digits=dp.get_precision('Product Unit of Measure'), default=0.0)
    qty_invoiced = fields.Float(string='Invoiced Quantity', store=True, readonly=True, digits=dp.get_precision('Product Unit of Measure'))
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
            self.work_center = self.product_id.work_center.name
            self.service_duration = self.product_id.service_duration

        return res
    

    # @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.price_unit
    #         taxes = line.tax_id.compute_all(price, line.repair_line_id.currency_id, line.product_uom_qty)
    #         line.update({
    #             'price_subtotal': taxes['total_excluded'],
    #         })


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

