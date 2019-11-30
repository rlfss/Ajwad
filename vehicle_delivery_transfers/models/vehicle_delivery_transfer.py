from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock_landed_costs.models import product
from odoo.exceptions import UserError


class VehicleDelivery(models.Model):
    _name = 'vehicle.delivery.transfer'
    _description = 'Vehicle Delivery Transfer'
    _inherit = 'mail.thread'

    name = fields.Char(
        'Name', default=lambda self: _('New'),
        copy=False, readonly=True, track_visibility='always')

    date = fields.Date(
        'Date', default=fields.Date.context_today,
        copy=False, required=True, states={'confirm': [('readonly', True)]}, track_visibility='onchange')

    picking_ids = fields.Many2one(
        'stock.picking', string='Transfers',
        copy=False,required=True, states={'confirm': [('readonly', True)]})

    partner_id = fields.Many2one('res.partner', string='Partner',states={'confirm': [('readonly', True)]},compute='_compute_partner_id')

    amount_total = fields.Integer(
        'Total',digits=0, store=True, track_visibility='always',compute='_compute_total_amount')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled')], 'State', default='draft',
        copy=False, readonly=True, track_visibility='onchange')

    delivery_lines = fields.One2many(
        'vehicle.delivery.lines', 'vehicle_id', 'Vehicle Delivery',states={'confirm': [('readonly', True)]})

    test = fields.Text('Test')

    lot_serial_number1 = fields.Many2one('stock.production.lot',string='LOT')

    id_number = fields.Char(string ='ID Number')
    expiry_date = fields.Date(string='Expiration')
    received_date = fields.Date(string='Received ')
    license_type = fields.Char(string='License Type')
    

    





    @api.one
    @api.depends('delivery_lines.quantity')
    def _compute_total_amount(self):
        self.amount_total = sum(line.quantity for line in self.delivery_lines)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.delivery.transfer')
        return super(VehicleDelivery, self).create(vals)


    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def button_validate(self):
        return self.write({'state': 'confirm'})

    @api.depends('picking_ids')
    def _compute_partner_id(self):
        if self.picking_ids:
            self.partner_id = self.picking_ids.partner_id.id


    @api.onchange('picking_ids')
    def get_change_delivery_line(self):
        new_lines = self.env['vehicle.delivery.lines']
        data = {}
        for line in self.picking_ids.move_ids_without_package.sorted(key=lambda m: m.product_id.id):
            for ml in line.move_line_ids:
                if ml.product_id.is_vehicle == True:
                    self.lot_serial_number1 = ml.lot_id.id
                    data = {
                    'product_id': ml.product_id.id,
                    'quantity': ml.qty_done,
                    'lot_serial_number':ml.lot_id.id
                    }
                    new_line = new_lines.new(data)
                    new_lines += new_line
        self.delivery_lines += new_lines

    @api.onchange('picking_ids')
    def onchange_partner_ids(self):
        selected = []
        res = {}
        stock_picking_lines = self.env['stock.picking'].search([])
        delivery_lines = self.search([])
        for line1 in stock_picking_lines:
                if line1.picking_type_code == 'outgoing' and line1.state == 'done':
                    selected.append(line1.name)
        if delivery_lines:
            for line in stock_picking_lines:
                for delivery in delivery_lines:
                    if line.name == delivery.picking_ids.name and line.picking_type_code == 'outgoing' and line.state == 'done':
                        selected.remove(line.name)
                        res.update({'domain':{
                                    'picking_ids':[('name','=',list(set(selected)))],
                                    }})


            return res

        else:
            for line in stock_picking_lines:
                if line.picking_type_code == 'outgoing' and line.state == 'done':
                    selected.append(line.name)
                    res.update({'domain':{
                                    'picking_ids':[('name','=',list(set(selected)))],
                                    }})
            return res


    @api.multi
    def action_view_vehicle_lines(self):
        for rec in self.delivery_lines:
            if rec.vehicle_id:
                seq =rec.env['ir.sequence'].next_by_code('vehicle.delivery.lines')
                rec.name =seq
        return {
                'name': _('Vehicle Check Report'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'vehicle.delivery.lines',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('vehicle_id','=',self.name)],
            }



        






class Products(models.Model):
    _inherit = 'product.product'

    delivery_ref = fields.Many2one('vehicle.delivery.transfer',string='Delivery Ref',compute='_compute_delivery_ref')


    def  _compute_delivery_ref(self):
        vehicle_ref_id = self.env['vehicle.delivery.lines'].search([])
        for line in vehicle_ref_id:
            if line.product_id.id == self.id:
                self.delivery_ref = line.vehicle_id.id



class TransferPickingLines(models.Model):
    _inherit = 'stock.move'
    def _prepare_delivery_line(self):
        pickings = self.env['stock.picking']
        x = pickings.move_ids_without_package.sorted(key=lambda m: m.product_id.id)
        data = {
            'product_id': self.product_id.id,
            'quantity': self.quantity_done,
            'lot_serial_number':x.move_line_ids.sorted(key=lambda ml: ml.location_id.id).lot_id.name
               }
        return data

class VehicleColor(models.Model):
    _name = 'vehicle.color'
    name = fields.Char('Color')

class VehicleMotor(models.Model):
    _name = 'vehicle.motor'
    name = fields.Char('Molor')

class VehicleDeliveryLine(models.Model):
    _name = 'vehicle.delivery.lines'
    _description = 'Vehicle Delivery Line'

    name = fields.Char('Name',copy=False,track_visibility='always',readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled')], 'State', default='draft',
        copy=False, readonly=True, track_visibility='onchange')

    product_id = fields.Many2one('product.product', 'Product', required=True)

    desc = fields.Char('Description')

    vehicle_id = fields.Many2one(
        'vehicle.delivery.transfer', 'Vehicle Delivery',
        required=True, ondelete='cascade', readonly=True)

    motor = fields.Many2one(
        'vehicle.motor', 'Motor', ondelete='cascade')

    color = fields.Many2one(
        'vehicle.color', 'Color', ondelete='cascade')

    quantity = fields.Integer("Quantity")

    lot_serial_number = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('product_id','=',product_id)]")

    delivery_ref = fields.Char(string='Delivery Ref' , compute='_compute_delivery_ref') 

    plate_num = fields.Char(string='Plate Number') 
    vehicle_model = fields.Char(string='Vehicle Model',compute='_compute_vehicle_make_model')
    vehicle_make = fields.Char(string='Vehicle Make',compute='_compute_vehicle_make_model')
    production_year = fields.Char(string='Production Year')
    vehicle_mileage = fields.Char(string='Vehicle Mileage')
    note = fields.Text(string='Note')





    @api.one
    def _compute_delivery_ref(self):
        for ref in self.vehicle_id:
            self.delivery_ref = self.vehicle_id.name

    @api.one
    def _compute_vehicle_make_model(self):
        str = self.product_id.name
        arr =str.split()
        self.vehicle_make= arr[0]
        if len(arr) > 1:
            self.vehicle_model= arr[1]
        else:
            self.vehicle_model= "None"

        

    @api.multi
    def button_cancel(self):
        return self.write({'state': 'cancel'})

    @api.multi
    def button_validate(self):
        return self.write({'state': 'confirm'})

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.delivery.transfer')
    #     return super(VehicleDelivery, self).create(vals)


    # @api.onchange('vehicle_id')
    # def _compute_seq(self):
    #     for rec in self:
    #         if rec.vehicle_id:
    #             seq =rec.env['ir.sequence'].next_by_code('vehicle.delivery.lines')
    #             rec.name =seq


    

    

